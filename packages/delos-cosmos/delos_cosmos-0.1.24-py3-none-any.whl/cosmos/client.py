"""Client for interacting with the Cosmos API."""

import json
from contextlib import suppress
from pathlib import Path
from typing import IO, Any, Callable, Literal, cast

import requests

from .endpoints import Endpoints, RequestMethod
from .exceptions import APIKeyMissingError, InvalidInputError
from .releases import AllReleases
from .settings import VerboseLevel, logger

COSMOS_PLATFORM_BACKEND_URL = "https://platform.cosmos-suite.ai"


class CosmosClient:
    """Client for interacting with the Cosmos API.

    Attributes:
        server_url: The URL of the server.
        apikey: The API key to be used for requests.

    """

    def __init__(
        self: "CosmosClient",
        apikey: str | None = None,
        server_url: str | None = COSMOS_PLATFORM_BACKEND_URL,
        verbose: VerboseLevel = VerboseLevel.INFO,
    ) -> None:
        """Initialize the client with the server URL and API key.

        Args:
            apikey: The API key to be used for requests.
            server_url: The URL of the server.
            verbose: The verbosity level of the client.
                0 - No logging
                1 - Only print the requests (default)
                2 - Print the requests and the response

        """
        if apikey is None:
            raise APIKeyMissingError

        self.apikey = apikey
        self.server_url = server_url
        self.verbose = verbose

        self.session = requests.Session()
        self.session.headers.update({"apikey": self.apikey})

        self._client_version = AllReleases[0]

    def _log(self: "CosmosClient", message: str, level: VerboseLevel = VerboseLevel.INFO) -> None:
        if self.verbose >= level:
            logger.debug(message)

    def _make_request(
        self: "CosmosClient",
        endpoint: tuple[str, RequestMethod],
        data: dict[str, Any] | None = None,
        files: Any = None,
        params: dict[str, Any] | None = None,
        **kwargs: Any,
    ) -> dict[str, Any] | None:
        """Make a request to the specified endpoint with the given data and files.

        Args:
            apikey: The Cosmos key to be used for the request.
            endpoint: A tuple containing the endpoint URL and the request type.
            data: The data to be sent in the request body (default is None).
            files: The files to be sent in the request (default is None).
            params: The query parameters to be sent in the request (default is None).
            kwargs: Specific keyword arguments to be passed to the request function.

        Returns:
            The response from the request as a dictionary, or None if an error occurred.

        """
        url = f"{self.server_url}{self._client_version.suffix}{endpoint[0]}"
        request_method = endpoint[1]

        request_func = cast(
            "Callable[..., requests.Response] | None",
            {
                RequestMethod.GET: self.session.get,
                RequestMethod.POST: self.session.post,
                RequestMethod.PUT: self.session.put,
                RequestMethod.DELETE: self.session.delete,
            }.get(request_method),
        )

        if not request_func:
            unsupported_method_error = f"Unsupported HTTP method: {request_method}"
            self._log(unsupported_method_error, level=VerboseLevel.DEBUG)
            raise ValueError(unsupported_method_error)

        if self.verbose >= VerboseLevel.DEBUG:
            files_details = [name for (param, (name, content)) in files] if files else ""
            files_message = f"{len(files)} Files: {files_details}" if files else "No files"

            self._log(f"Request URL: {url}", VerboseLevel.DEBUG)
            self._log(f"Request Method: {request_method}", VerboseLevel.DEBUG)
            self._log(f"Request Data: {data}", VerboseLevel.DEBUG)
            self._log(f"Request Files: {files_message}", VerboseLevel.DEBUG)
            self._log(f"Request Params: {params}", VerboseLevel.DEBUG)

        response = None

        try:
            # Handle both regular form data and multipart form data
            form_data = {}
            if data:
                # Convert all data values to strings for form data
                form_data.update({k: str(v) if v is not None else "" for k, v in data.items()})

            response = request_func(
                url,
                data=form_data,
                files=files,
                params=params,
                **kwargs,
            )

            response.raise_for_status()

            if self.verbose >= VerboseLevel.INFO:
                self._log(f"Response: {response.json()}", VerboseLevel.INFO)
            return response.json()

        except requests.exceptions.RequestException as e:
            logger.error(f"Request Error: {e}")
            with suppress(NameError):
                logger.error(f"Response Content: {response.text if response else 'No response'}")
            raise

    @staticmethod
    def _get_files_from_paths(filepaths: list[Path] | list[str]) -> list[tuple[str, tuple[str, IO[bytes]]]]:
        """Read the files from given filepaths.

        Args:
            filepaths: The list of paths to be converted to files.

        Returns:
            The list of files.

        """
        files_paths = [Path(filepath) if isinstance(filepath, str) else filepath for filepath in filepaths]
        return [("files", (filepath.name, filepath.open("rb"))) for filepath in files_paths]

    def status_health_request(
        self: "CosmosClient",
    ) -> dict[str, Any] | None:
        """Make a request to check the health of the server."""
        return self._make_request(Endpoints.STATUS.HEALTH.value)

    def translate_text_request(
        self: "CosmosClient",
        text: str,
        output_language: str,
        input_language: str | None = None,
    ) -> dict[str, Any] | None:
        """Make a request to translate text.

        Args:
            text: The text to be translated.
            output_language: The output language for the translation.
            input_language: The input language for the translation (Optional).

        Returns:
            The server response.

        """
        data = {
            "text": text,
            "output_language": output_language,
        }
        if input_language:
            data["input_language"] = input_language
        return self._make_request(endpoint=Endpoints.TRANSLATE.TRANSLATE_TEXT.value, data=data)

    def translate_file_request(
        self: "CosmosClient",
        filepath: Path | str,
        output_language: str,
        input_language: str | None = None,
        return_type: Literal["raw_text", "url", "file"] = "raw_text",
    ) -> dict[str, Any] | None:
        """Make a request to translate a file.

        Args:
            filepath: The file path to be translated.
            output_language: The output language for the translation.
            input_language: The input language for the translation (Optional).
            return_type: The type of return for the translation (Optional). Default is "raw_text".

        Returns:
            The server response.

        """
        data = {
            "output_language": output_language,
            "return_type": return_type,
        }
        if input_language:
            data["input_language"] = input_language

        file_path = Path(filepath) if isinstance(filepath, str) else filepath
        files = [("file", (file_path.name, file_path.open("rb")))]

        return self._make_request(Endpoints.TRANSLATE.TRANSLATE_FILE.value, data=data, files=files)

    def web_search_request(
        self: "CosmosClient",
        text: str,
        output_language: str | None = None,
        desired_urls: list[str] | str | None = None,
    ) -> dict[str, Any] | None:
        """Make a request to perform a search.

        Args:
            text: The text to be searched.
            output_language: The output language for the search (Optional).
            desired_urls: The desired URLs to be priviledged in the search (Optional).

        Returns:
            The server response.

        """
        data = {"text": text}
        if output_language:
            data["output_language"] = output_language
        if desired_urls:
            data["desired_urls"] = str(desired_urls)

        return self._make_request(Endpoints.WEB.SEARCH.value, data)

    def llm_chat_request(
        self: "CosmosClient",
        text: str,
        model: str | None = None,
        **kwargs: Any,
    ) -> dict[str, Any] | None:
        """Make a request to chat with the LLM.

        Args:
            text: The text to be chatted.
            model: The model to be used for chatting (Optional).
            kwargs: Specific keyword arguments to be passed to the request function.
                For example: `response_format = {"type":"json_object"}` or `temperature=0.5

        Returns:
            The server response.

        """
        data = {"text": text}
        if model:
            data["model"] = model
        if kwargs:
            data["kwargs"] = str(kwargs)
        return self._make_request(endpoint=Endpoints.LLM.CHAT.value, data=data)

    def llm_embed_request(
        self: "CosmosClient",
        text: str,
    ) -> dict[str, Any] | None:
        """Make a request to embed data using the LLM.

        Args:
            text: The text to be embedded.

        Returns:
            The server response.

        """
        return self._make_request(Endpoints.LLM.EMBED.value, data={"text": text})

    def files_parse_request(
        self: "CosmosClient",
        filepath: Path,
        extract_type: Literal["subchunks", "chunks", "pages", "file"] = "chunks",
        read_images: Literal["no", "transcript"] = "no",
        k_min: int | None = None,
        k_max: int | None = None,
        overlap: int | None = None,
        filter_pages: str | None = None,
    ) -> dict[str, Any] | None:
        """Make a request to chunk a file.

        Args:
            filepath: The file path to be chunked.
            extract_type: The type of extraction to be performed (Optional). Default is "chunks".
            read_images: Whether to read images from the files.
            k_min: The minimum number of chunks to be extracted (Optional). Default is 500 tokens.
            k_max: The maximum number of chunks to be extracted (Optional). Default is 1000 tokens.
            overlap: The overlap between chunks (Optional). Default is 10 tokens.
            filter_pages: The filter for pages (Optional). Default is all pages.

        Returns:
            The server response.

        """
        files = [("file", (filepath.name, filepath.open("rb")))]
        data = {
            "extract_type": extract_type,
            "read_images": read_images,
            "k_min": k_min,
            "k_max": k_max,
            "overlap": overlap,
            "filter_pages": filter_pages,
        }
        return self._make_request(Endpoints.FILES.PARSER.value, data=data, files=files)

    def files_index_create_request(
        self: "CosmosClient",
        name: str,
        read_images: Literal["no", "transcript"] = "no",
        filepaths: list[Path] | list[str] | None = None,
        filesobjects: list[tuple[str, tuple[str, IO[bytes]]]] | None = None,
    ) -> dict[str, Any] | None:
        """Make a request to create an index.

        Args:
            name: The name of the index.
            read_images: Whether to read images from the files.
            filepaths: A list of file paths to be indexed. Provide either filepaths or filesobjects, not both.
            filesobjects: A list of file objects to be indexed.

        Returns:
            The server response.

        """
        if not filepaths and not filesobjects:
            error_message = "Either filepaths or filesobjects must be provided."
            raise InvalidInputError(error_message)

        if filepaths and filesobjects:
            error_message = "Provide either filepaths or filesobjects, not both."
            raise InvalidInputError(error_message)

        files = []
        if filepaths:
            for fp in filepaths:
                path = Path(fp) if isinstance(fp, str) else fp
                with path.open("rb") as file:
                    files.append(("files", (path.name, file.read())))
        elif filesobjects:
            for _, (filename, file_object) in filesobjects:
                files.append(("files", (filename, file_object.read())))

        return self._make_request(
            Endpoints.FILES.INDEX_CREATE.value,
            data={"name": name, "read_images": read_images},
            files=files,
        )

    def files_index_add_files_request(
        self: "CosmosClient",
        index_uuid: str,
        read_images: Literal["no", "transcript"] = "no",
        filepaths: list[Path] | list[str] | None = None,
        filesobjects: list[tuple[str, tuple[str, IO[bytes]]]] | None = None,
    ) -> dict[str, Any] | None:
        """Make a request to add files to an index.

        Args:
            index_uuid: The index UUID.
            read_images: Whether to read images from the files.
            filepaths: A list of file paths to be added to the index.
                        Provide either filepaths or filesobjects, not both.
            filesobjects: A list of file objects to be indexed.

        Returns:
            The server response.

        """
        if not filepaths and not filesobjects:
            error_message = "Either filepaths or filesobjects must be provided."
            raise InvalidInputError(error_message)

        if filepaths and filesobjects:
            error_message = "Provide either filepaths or filesobjects, not both."
            raise InvalidInputError(error_message)

        files = []
        if filepaths:
            for fp in filepaths:
                path = Path(fp) if isinstance(fp, str) else fp
                with path.open("rb") as file:
                    files.append(("files", (path.name, file.read())))
        elif filesobjects:
            for _, (filename, file_object) in filesobjects:
                files.append(("files", (filename, file_object.read())))

        return self._make_request(
            Endpoints.FILES.INDEX_ADD_FILES.value,
            data={"index_uuid": index_uuid, "read_images": read_images},
            files=files,
        )

    def files_index_delete_files_request(
        self: "CosmosClient",
        index_uuid: str,
        files_hashes: list[str],
    ) -> dict[str, Any] | None:
        """Make a request to delete files from an index.

        Args:
            index_uuid: The index UUID.
            files_hashes: A list of file hashes to be deleted from the index.

        Returns:
            The server response.

        """
        logger.warning(
            f"{len(files_hashes)} Files to be deleted: {files_hashes} (type {type(files_hashes)} "
            f"- first item:{files_hashes[0]} ({type(files_hashes[0])}))",
        )
        files_hashes_str = [str(file_hash) for file_hash in files_hashes]
        data = {"index_uuid": index_uuid, "files_hashes": files_hashes_str}
        return self._make_request(Endpoints.FILES.INDEX_DELETE_FILES.value, data=data)

    def files_index_delete_request(self: "CosmosClient", index_uuid: str) -> dict[str, Any] | None:
        """Make a request to delete an index.

        Args:
            index_uuid: The index UUID.

        Returns:
            The server response.

        """
        data = {"index_uuid": index_uuid}
        return self._make_request(Endpoints.FILES.INDEX_DELETE.value, data=data)

    def files_index_restore_request(self: "CosmosClient", index_uuid: str) -> dict[str, Any] | None:
        """Make a request to restore an index.

        Args:
            index_uuid: The index UUID.

        Returns:
            The server response.

        """
        data = {"index_uuid": index_uuid}
        return self._make_request(Endpoints.FILES.INDEX_RESTORE.value, data=data)

    def files_index_rename_request(
        self: "CosmosClient",
        index_uuid: str,
        name: str,
    ) -> dict[str, Any] | None:
        """Make a request to rename an index.

        Args:
            index_uuid: The index UUID.
            name: The new name for the index.

        Returns:
            The server response.

        """
        data = {"index_uuid": index_uuid, "name": name}
        return self._make_request(Endpoints.FILES.INDEX_RENAME.value, data=data)

    def files_index_ask_request(
        self: "CosmosClient",
        index_uuid: str,
        question: str,
        output_language: str | None = None,
        active_files: list[str] | str = "all",
    ) -> dict[str, Any] | None:
        """Make a request to ask a question about the index contents.

        Args:
            index_uuid: The index UUID.
            question: The question to be asked.
            output_language: The output language for the question.
            active_files: The hashes of the files to be used for the question. Or "all" (default) or "none".

        Returns:
            The server response.

        """
        data = {
            "index_uuid": str(index_uuid),
            "question": question,
            "active_files": json.dumps(active_files) if isinstance(active_files, list) else active_files,
        }
        if output_language:
            data["output_language"] = output_language

        return self._make_request(Endpoints.FILES.INDEX_ASK.value, data=data)

    def files_index_embed_request(self: "CosmosClient", index_uuid: str) -> dict[str, Any] | None:
        """Make a request to embed an index.

        Args:
            index_uuid: The index UUID.

        Returns:
            The server response.

        """
        data = {"index_uuid": index_uuid}
        return self._make_request(Endpoints.FILES.INDEX_EMBED.value, data=data)

    def files_index_details_request(self: "CosmosClient", index_uuid: str) -> dict[str, Any] | None:
        """Make a request to get details of an index.

        Args:
            index_uuid: The index UUID.

        Returns:
            The server response.

        """
        params = {"index_uuid": index_uuid}
        return self._make_request(Endpoints.FILES.INDEX_DETAILS.value, params=params)

    def files_index_list_request(self: "CosmosClient") -> dict[str, Any] | None:
        """Make a request to list all indexes."""
        return self._make_request(Endpoints.FILES.INDEX_LIST.value)
