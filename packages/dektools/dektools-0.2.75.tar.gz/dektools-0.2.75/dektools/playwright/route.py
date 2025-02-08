# https://github.com/Kaliiiiiiiiii-Vinyzu/patchright-python/issues/9
import copy
import os
from ..str import Fragment
from ..web.headers import quick_split_ct
from ..web.status import is_redirect, HTTP_200_OK
from ..web.html import get_redirect_html
from .common import AsyncPlaywrightResponse, is_stealth


async def fix_stealth_mode(context):
    if is_stealth(context):
        await RouteTool(True).context_route_all(context)


class RouteTool:
    marker_script_content = '(()=>{var _ = "7WG1smGqCQT3tV4yJeYVYT95VOWiChcMsjcQz27hMIgGyO3iLQY5ZNyIqPxCnAMW"})();'

    def __init__(self, stealth):
        self._is_stealth = stealth

    async def _error_add_script(self, *args, **kwargs):
        raise ValueError('No more add_init_script should be called')

    async def fix_blank_jump(self, context):
        if self._is_stealth:
            await context.add_init_script(script="""
document.addEventListener('click', function (e) {
    if (!e.ctrlKey) {
        var cursor = e.target
        while (cursor) {
            if (cursor.tagName === 'A') {
                if (cursor.getAttribute('target') === '_blank') {
                    window.open(cursor.href, '_blank')
                    e.preventDefault()
                }
                break
            }
            cursor = cursor.parentElement
        }
    }
});""")

    @classmethod
    def fix_package(cls, reverse=False):
        import patchright
        from ..file import read_text, write_file
        path_file = os.path.join(
            os.path.dirname(os.path.abspath(patchright.__file__)),
            'driver/package/lib/server/chromium/crNetworkManager.js'
        )
        content = read_text(path_file)
        replace = [
            [
                "const isTextHtml = response.headers.some(header => header.name === 'content-type' && "
                "header.value.includes('text/html'));",
                """const index = response.headers.findIndex(header => header.name == '--add-script-inject--' && """
                """header.value == 'true');
let isTextHtml = false
if (index !== -1){
  response.headers.splice(index, 1)
  isTextHtml = true
}"""],
            [
                "      allInjections.forEach(",
                "allInjections.push({source:'%s'});allInjections.forEach(" % cls.marker_script_content],
            ["        injectionHTML += `<script", "        if(isTextHtml)injectionHTML += `<script"]
        ]
        content = Fragment.replace_safe_again(content, replace, reverse)
        if content is not None:
            write_file(path_file, s=content)

    def fixed_headers(self, request, headers):
        if self._is_stealth and (request is None or self.is_route_special_request(request)):
            headers = copy.deepcopy(headers)
            headers['--add-script-inject--'] = 'true'
            return headers
        return headers

    def fix_body(self, body):
        if self._is_stealth:
            marker = ("%s</script>" % self.marker_script_content).encode('utf-8')
            try:
                frag = Fragment(body, marker, sep=True)
                return frag[2]
            except IndexError:
                pass
        return body

    @staticmethod
    def transform_redirects(response):
        if not is_redirect(response.status):
            return response
        headers = response.headers.copy()
        target = headers.pop('location')
        headers['content-type'] = 'text/html'
        return AsyncPlaywrightResponse(response.url, HTTP_200_OK, headers, get_redirect_html(target).encode('utf-8'))

    @staticmethod
    def is_route_special_request(request):
        return (
                request.resource_type == "document" and
                request.url.startswith("http") and
                request.method == 'GET' and
                quick_split_ct(request.headers.get('content-type', ''))[0] not in {
                    "application/x-www-form-urlencoded",
                    "multipart/form-data",
                }
        )

    async def context_route_all(self, context, default=None, hit=None, get_response=None):
        async def default_get_response(route):
            return await context.request.get(route.request.url, max_redirects=0)

        async def route_handler(route):
            if self.is_route_special_request(route.request):
                if get_response is None:
                    response = await default_get_response(route)
                else:
                    response = await get_response(route, context, default_get_response)
                if response is not None:
                    response = self.transform_redirects(response)
                if hit is not None:
                    await hit(route, response)
                if response is not None:
                    if isinstance(response, AsyncPlaywrightResponse):
                        kwargs = response.fulfill_kwargs()
                    else:
                        kwargs = dict(response=response)
                    kwargs['headers'] = self.fixed_headers(None, response.headers)
                    await route.fulfill(**kwargs)
            else:
                if default is None:
                    await route.continue_()
                else:
                    await default(route)

        if self._is_stealth:
            context._impl_obj.route_injecting = True
            await context.route("**/*", route_handler)
        else:
            if default is not None:
                await context.route("**/*", default)
