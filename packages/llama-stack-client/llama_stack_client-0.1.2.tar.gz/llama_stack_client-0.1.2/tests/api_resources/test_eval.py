# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from __future__ import annotations

import os
from typing import Any, cast

import pytest

from tests.utils import assert_matches_type
from llama_stack_client import LlamaStackClient, AsyncLlamaStackClient
from llama_stack_client.types import (
    Job,
    EvaluateResponse,
)

base_url = os.environ.get("TEST_API_BASE_URL", "http://127.0.0.1:4010")


class TestEval:
    parametrize = pytest.mark.parametrize("client", [False, True], indirect=True, ids=["loose", "strict"])

    @parametrize
    def test_method_evaluate_rows(self, client: LlamaStackClient) -> None:
        eval = client.eval.evaluate_rows(
            task_id="task_id",
            input_rows=[{"foo": True}],
            scoring_functions=["string"],
            task_config={
                "eval_candidate": {
                    "model": "model",
                    "sampling_params": {"strategy": {"type": "greedy"}},
                    "type": "model",
                },
                "type": "benchmark",
            },
        )
        assert_matches_type(EvaluateResponse, eval, path=["response"])

    @parametrize
    def test_method_evaluate_rows_with_all_params(self, client: LlamaStackClient) -> None:
        eval = client.eval.evaluate_rows(
            task_id="task_id",
            input_rows=[{"foo": True}],
            scoring_functions=["string"],
            task_config={
                "eval_candidate": {
                    "model": "model",
                    "sampling_params": {
                        "strategy": {"type": "greedy"},
                        "max_tokens": 0,
                        "repetition_penalty": 0,
                    },
                    "type": "model",
                    "system_message": {
                        "content": "string",
                        "role": "system",
                    },
                },
                "type": "benchmark",
                "num_examples": 0,
            },
        )
        assert_matches_type(EvaluateResponse, eval, path=["response"])

    @parametrize
    def test_raw_response_evaluate_rows(self, client: LlamaStackClient) -> None:
        response = client.eval.with_raw_response.evaluate_rows(
            task_id="task_id",
            input_rows=[{"foo": True}],
            scoring_functions=["string"],
            task_config={
                "eval_candidate": {
                    "model": "model",
                    "sampling_params": {"strategy": {"type": "greedy"}},
                    "type": "model",
                },
                "type": "benchmark",
            },
        )

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        eval = response.parse()
        assert_matches_type(EvaluateResponse, eval, path=["response"])

    @parametrize
    def test_streaming_response_evaluate_rows(self, client: LlamaStackClient) -> None:
        with client.eval.with_streaming_response.evaluate_rows(
            task_id="task_id",
            input_rows=[{"foo": True}],
            scoring_functions=["string"],
            task_config={
                "eval_candidate": {
                    "model": "model",
                    "sampling_params": {"strategy": {"type": "greedy"}},
                    "type": "model",
                },
                "type": "benchmark",
            },
        ) as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            eval = response.parse()
            assert_matches_type(EvaluateResponse, eval, path=["response"])

        assert cast(Any, response.is_closed) is True

    @parametrize
    def test_path_params_evaluate_rows(self, client: LlamaStackClient) -> None:
        with pytest.raises(ValueError, match=r"Expected a non-empty value for `task_id` but received ''"):
            client.eval.with_raw_response.evaluate_rows(
                task_id="",
                input_rows=[{"foo": True}],
                scoring_functions=["string"],
                task_config={
                    "eval_candidate": {
                        "model": "model",
                        "sampling_params": {"strategy": {"type": "greedy"}},
                        "type": "model",
                    },
                    "type": "benchmark",
                },
            )

    @parametrize
    def test_method_run_eval(self, client: LlamaStackClient) -> None:
        eval = client.eval.run_eval(
            task_id="task_id",
            task_config={
                "eval_candidate": {
                    "model": "model",
                    "sampling_params": {"strategy": {"type": "greedy"}},
                    "type": "model",
                },
                "type": "benchmark",
            },
        )
        assert_matches_type(Job, eval, path=["response"])

    @parametrize
    def test_method_run_eval_with_all_params(self, client: LlamaStackClient) -> None:
        eval = client.eval.run_eval(
            task_id="task_id",
            task_config={
                "eval_candidate": {
                    "model": "model",
                    "sampling_params": {
                        "strategy": {"type": "greedy"},
                        "max_tokens": 0,
                        "repetition_penalty": 0,
                    },
                    "type": "model",
                    "system_message": {
                        "content": "string",
                        "role": "system",
                    },
                },
                "type": "benchmark",
                "num_examples": 0,
            },
        )
        assert_matches_type(Job, eval, path=["response"])

    @parametrize
    def test_raw_response_run_eval(self, client: LlamaStackClient) -> None:
        response = client.eval.with_raw_response.run_eval(
            task_id="task_id",
            task_config={
                "eval_candidate": {
                    "model": "model",
                    "sampling_params": {"strategy": {"type": "greedy"}},
                    "type": "model",
                },
                "type": "benchmark",
            },
        )

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        eval = response.parse()
        assert_matches_type(Job, eval, path=["response"])

    @parametrize
    def test_streaming_response_run_eval(self, client: LlamaStackClient) -> None:
        with client.eval.with_streaming_response.run_eval(
            task_id="task_id",
            task_config={
                "eval_candidate": {
                    "model": "model",
                    "sampling_params": {"strategy": {"type": "greedy"}},
                    "type": "model",
                },
                "type": "benchmark",
            },
        ) as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            eval = response.parse()
            assert_matches_type(Job, eval, path=["response"])

        assert cast(Any, response.is_closed) is True

    @parametrize
    def test_path_params_run_eval(self, client: LlamaStackClient) -> None:
        with pytest.raises(ValueError, match=r"Expected a non-empty value for `task_id` but received ''"):
            client.eval.with_raw_response.run_eval(
                task_id="",
                task_config={
                    "eval_candidate": {
                        "model": "model",
                        "sampling_params": {"strategy": {"type": "greedy"}},
                        "type": "model",
                    },
                    "type": "benchmark",
                },
            )


class TestAsyncEval:
    parametrize = pytest.mark.parametrize("async_client", [False, True], indirect=True, ids=["loose", "strict"])

    @parametrize
    async def test_method_evaluate_rows(self, async_client: AsyncLlamaStackClient) -> None:
        eval = await async_client.eval.evaluate_rows(
            task_id="task_id",
            input_rows=[{"foo": True}],
            scoring_functions=["string"],
            task_config={
                "eval_candidate": {
                    "model": "model",
                    "sampling_params": {"strategy": {"type": "greedy"}},
                    "type": "model",
                },
                "type": "benchmark",
            },
        )
        assert_matches_type(EvaluateResponse, eval, path=["response"])

    @parametrize
    async def test_method_evaluate_rows_with_all_params(self, async_client: AsyncLlamaStackClient) -> None:
        eval = await async_client.eval.evaluate_rows(
            task_id="task_id",
            input_rows=[{"foo": True}],
            scoring_functions=["string"],
            task_config={
                "eval_candidate": {
                    "model": "model",
                    "sampling_params": {
                        "strategy": {"type": "greedy"},
                        "max_tokens": 0,
                        "repetition_penalty": 0,
                    },
                    "type": "model",
                    "system_message": {
                        "content": "string",
                        "role": "system",
                    },
                },
                "type": "benchmark",
                "num_examples": 0,
            },
        )
        assert_matches_type(EvaluateResponse, eval, path=["response"])

    @parametrize
    async def test_raw_response_evaluate_rows(self, async_client: AsyncLlamaStackClient) -> None:
        response = await async_client.eval.with_raw_response.evaluate_rows(
            task_id="task_id",
            input_rows=[{"foo": True}],
            scoring_functions=["string"],
            task_config={
                "eval_candidate": {
                    "model": "model",
                    "sampling_params": {"strategy": {"type": "greedy"}},
                    "type": "model",
                },
                "type": "benchmark",
            },
        )

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        eval = await response.parse()
        assert_matches_type(EvaluateResponse, eval, path=["response"])

    @parametrize
    async def test_streaming_response_evaluate_rows(self, async_client: AsyncLlamaStackClient) -> None:
        async with async_client.eval.with_streaming_response.evaluate_rows(
            task_id="task_id",
            input_rows=[{"foo": True}],
            scoring_functions=["string"],
            task_config={
                "eval_candidate": {
                    "model": "model",
                    "sampling_params": {"strategy": {"type": "greedy"}},
                    "type": "model",
                },
                "type": "benchmark",
            },
        ) as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            eval = await response.parse()
            assert_matches_type(EvaluateResponse, eval, path=["response"])

        assert cast(Any, response.is_closed) is True

    @parametrize
    async def test_path_params_evaluate_rows(self, async_client: AsyncLlamaStackClient) -> None:
        with pytest.raises(ValueError, match=r"Expected a non-empty value for `task_id` but received ''"):
            await async_client.eval.with_raw_response.evaluate_rows(
                task_id="",
                input_rows=[{"foo": True}],
                scoring_functions=["string"],
                task_config={
                    "eval_candidate": {
                        "model": "model",
                        "sampling_params": {"strategy": {"type": "greedy"}},
                        "type": "model",
                    },
                    "type": "benchmark",
                },
            )

    @parametrize
    async def test_method_run_eval(self, async_client: AsyncLlamaStackClient) -> None:
        eval = await async_client.eval.run_eval(
            task_id="task_id",
            task_config={
                "eval_candidate": {
                    "model": "model",
                    "sampling_params": {"strategy": {"type": "greedy"}},
                    "type": "model",
                },
                "type": "benchmark",
            },
        )
        assert_matches_type(Job, eval, path=["response"])

    @parametrize
    async def test_method_run_eval_with_all_params(self, async_client: AsyncLlamaStackClient) -> None:
        eval = await async_client.eval.run_eval(
            task_id="task_id",
            task_config={
                "eval_candidate": {
                    "model": "model",
                    "sampling_params": {
                        "strategy": {"type": "greedy"},
                        "max_tokens": 0,
                        "repetition_penalty": 0,
                    },
                    "type": "model",
                    "system_message": {
                        "content": "string",
                        "role": "system",
                    },
                },
                "type": "benchmark",
                "num_examples": 0,
            },
        )
        assert_matches_type(Job, eval, path=["response"])

    @parametrize
    async def test_raw_response_run_eval(self, async_client: AsyncLlamaStackClient) -> None:
        response = await async_client.eval.with_raw_response.run_eval(
            task_id="task_id",
            task_config={
                "eval_candidate": {
                    "model": "model",
                    "sampling_params": {"strategy": {"type": "greedy"}},
                    "type": "model",
                },
                "type": "benchmark",
            },
        )

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        eval = await response.parse()
        assert_matches_type(Job, eval, path=["response"])

    @parametrize
    async def test_streaming_response_run_eval(self, async_client: AsyncLlamaStackClient) -> None:
        async with async_client.eval.with_streaming_response.run_eval(
            task_id="task_id",
            task_config={
                "eval_candidate": {
                    "model": "model",
                    "sampling_params": {"strategy": {"type": "greedy"}},
                    "type": "model",
                },
                "type": "benchmark",
            },
        ) as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            eval = await response.parse()
            assert_matches_type(Job, eval, path=["response"])

        assert cast(Any, response.is_closed) is True

    @parametrize
    async def test_path_params_run_eval(self, async_client: AsyncLlamaStackClient) -> None:
        with pytest.raises(ValueError, match=r"Expected a non-empty value for `task_id` but received ''"):
            await async_client.eval.with_raw_response.run_eval(
                task_id="",
                task_config={
                    "eval_candidate": {
                        "model": "model",
                        "sampling_params": {"strategy": {"type": "greedy"}},
                        "type": "model",
                    },
                    "type": "benchmark",
                },
            )
