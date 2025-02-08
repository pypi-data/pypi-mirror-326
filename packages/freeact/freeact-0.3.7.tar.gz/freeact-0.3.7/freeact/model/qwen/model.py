import os
from typing import Any, Dict

from freeact.model.generic.model import GenericModel
from freeact.model.qwen.prompt import (
    EXECUTION_ERROR_TEMPLATE,
    EXECUTION_OUTPUT_TEMPLATE,
    SYSTEM_TEMPLATE,
)


class QwenCoder(GenericModel):
    """A specialized implementation of `GenericModel` for Qwen's Coder models.

    This class configures `GenericModel` specifically for use with Qwen 2.5 Coder models,
    It has been tested with *QwenCoder 2.5 Coder 32B Instruct*. Smaller models
    in this series may require adjustments to the prompt templates.

    Args:
        model_name: The provider-specific name of the Qwen model to use.
        api_key: Optional API key for Qwen. If not provided, reads from QWEN_API_KEY environment variable.
        base_url: Optional base URL for the API. If not provided, reads from QWEN_BASE_URL environment variable.
        skill_sources: Optional string containing Python skill module information to include in system template.
        system_template: Prompt template for the system message that guides the model to generate code actions.
            Must define a `{python_modules}` placeholder for the skill sources.
        execution_output_template: Prompt template for formatting execution outputs.
            Must define an `{execution_feedback}` placeholder.
        execution_error_template: Prompt template for formatting execution errors.
            Must define an `{execution_feedback}` placeholder.
        run_kwargs: Optional dictionary of additional arguments passed to the model's
            `request` and `feedback` methods. Defaults to a stop sequence that prevents
            the model from guessing code execution outputs.
        **kwargs: Additional keyword arguments passed to the `GenericModel` constructor.
    """

    def __init__(
        self,
        model_name: str,
        api_key: str | None = None,
        base_url: str | None = None,
        skill_sources: str | None = None,
        system_template: str = SYSTEM_TEMPLATE,
        execution_output_template: str = EXECUTION_OUTPUT_TEMPLATE,
        execution_error_template: str = EXECUTION_ERROR_TEMPLATE,
        run_kwargs: Dict[str, Any] | None = {"stop": ["```output"]},
        **kwargs,
    ):
        super().__init__(
            model_name=model_name,
            api_key=api_key or os.getenv("QWEN_API_KEY"),
            base_url=base_url or os.getenv("QWEN_BASE_URL"),
            execution_output_template=execution_output_template,
            execution_error_template=execution_error_template,
            system_message=system_template.format(python_modules=skill_sources or ""),
            run_kwargs=run_kwargs,
            **kwargs,
        )
