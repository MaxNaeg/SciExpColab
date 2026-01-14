
import matplotlib.pyplot as plt
import jax
import jax.numpy as jnp
import numpy as np
import matplotlib
import scipy
from tool_utils import exec_with_error_line
from sciexplorer.tool_utils import ImageData, get_image


SHOW_PLOTS = True


def execute_code(_fields:dict, code: str) -> dict: # type hints are imprtant and used by the agent
    # This is a tool. Its docstring and typehints will be automatically parsed to create the tool description for the agent.
    # When using _fields as an input argument, the framework will automatically pass all previously saved fields to the tool.
    # Additionally, the final tool description will automatically ask the agent to provide a label under which the result should be saved.
    # Tools always need to return dictionaries!
    """ Evaluate python code.
        This code can be e.g. be used to transform the previously saved fields or to calculate or save new fields.
        You can not see any plots created with this tool.
        The following variables are available during evaluation:
            all previosuly saved fields with their previously stated result_key as variable names (as global variables).
            jax: jax for numerical operations.
            jnp: jax.numpy for numerical operations.
            np: numpy for numerical operations.
            scipy: scipy for numerical operations including optimization and solving differential equations.
        IMPORTANT: Your code must set the variable 'result' to a dictionary in the end which should contain the newly generated data, for example: result={'<result_key>': <data>, ...}.
        Args:
            code: python code that sets the result variable to a dictionary containing some newly generated data.
        Returns:
            The result dictionary.
        """
    # This is a generic code block the execute some code with access to previously defined variables and previously saved fields.
    globals_dict = _fields | {'result':None, 'jax':jax, 'jnp': jnp, 'np':np, 'scipy':scipy}
    globals_dict = exec_with_error_line(code, globals_dict)
    if globals_dict['result'] is None:
        raise ValueError("The code did not set the result variable. It must be set to a dictionary containing the newly generated data. E.g. result={'<result_key>': <data>, ...}")
    if not isinstance(globals_dict['result'], dict):
        raise ValueError("The result variable must be a dictionary. E.g. result={'<result_key>': <data>, ...}")
    return globals_dict['result']

def plot_from_code(_fields:dict, code: str) -> dict: # type hints are imprtant and used by the agent
        # This is a tool. Its docstring and typehints will be automatically parsed to create the tool description for the agent.
        # When using _fields as an input argument, the framework will automatically pass all previously saved fields to the tool.
        # Additionally, the final tool description will automatically ask the agent to provide a label under which the result should be saved.
        # Tools always need to return dictionaries!
    """
    Execute python code that produces a plot from one or more previously saved arrays.
    The following variables are available during evaluation:
        all previosuly saved fields with their previously stated result_key as variable names (as global variables).
    You may use the following libraries:
        matplotlib: for plotting.
        matplotlib.pyplot as plt: for plotting.
        jax: for numerical operations.
        jax.numpy: for numerical operations.
        numpy: for numerical operations.
    Args:
        code: python code that produces a plot (without a plt.show() call!).
    Returns:
        Image
    """
    globals_dict = _fields | {'matplotlib': matplotlib, 'plt': plt, 'jax': jax, 'jnp': jnp, 'np': np}
    globals_dict = exec_with_error_line(code, globals_dict)
    Image = get_image()
    if SHOW_PLOTS:
        plt.show()
    return {'image': Image}

