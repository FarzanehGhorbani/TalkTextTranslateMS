import logging
from typing import Any
from fastapi.responses import UJSONResponse
from ujson import dumps
from ..proxies.proxies import message as proxi_message
import typing


class ResponseObject:
    def __new__(
        cls, data: Any = None, message: Any = None, status_code: int = 200
    ) -> Any:
        """This is a response object that get message and data, then
        return only data and push detail to message proxy.

        Args:
            data (Any): response data.
            detail (Any): response message.

        Returns:
            Any: response data.
        """
        if message:
            proxi_message(message)
        proxi_message(dict(status_code=status_code))
        return data


class Response(UJSONResponse):
    media_type = "application/json"

    def __init__(
        self,
        content: typing.Any = None,
        status_code: int = 200,
        headers: typing.Optional[typing.Dict[str, str]] = None,
        media_type: typing.Optional[str] = None,
        background=None,
    ) -> None:
        super().__init__(content, status_code, headers, media_type, background)

    def dumps(self, content):
        result: bool = True
        prepared_messages: list = proxi_message.get_private_stack()
        btsatus: int = None
        if not (self.status_code >= 200 and self.status_code < 300):
            result = False
        final_msgs = dict()
        validations = dict()

        for m in prepared_messages:
            if isinstance(m, dict):
                if "status_code" in m:
                    btsatus = m["status_code"]
                    break
                general = m.get("general", None)
                if general:
                    final_msgs.update(m)
                else:
                    validations.update(m)
            else:
                final_msgs.update({"general": m})
        final_msgs.update({"validations": validations}) if validations else None
        status = btsatus if btsatus else self.status_code

        # print(final_msgs.get("general"))
        
        if (
            not result
            and not final_msgs.get("general")
            and "Internal Server Error" in prepared_messages
        ):
            final_msgs["general"] = "Internal Server Error"
            if status == 200:
                btsatus = 500

        data = dict(
            data=content,
            result=result,
            message=final_msgs.get("general", None),
            status_code=btsatus if btsatus else self.status_code,
            errors=final_msgs.get("validations", {}),
        )
        # logging.info(data)
        return dumps(data).encode("utf-8")

    def render(self, content: Any) -> bytes:
        return self.dumps(content)
