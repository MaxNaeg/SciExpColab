import traceback
import linecache

def exec_with_error_line(code, globals, filename="<exec_block>"):
    # Register the code with linecache so traceback can look it up
    linecache.cache[filename] = (
        len(code),              # size
        None,                   # mtime (not important)
        code.splitlines(True),  # list of lines WITH newlines
        filename
    )

    try:
        compiled = compile(code, filename, "exec")
        exec(compiled, globals)
        return globals
    except Exception as e:
        error_message = ""
        tb = traceback.extract_tb(e.__traceback__)
        tb = [frame for frame in tb if frame.filename == filename]
        if not tb:
            error_message += "Unknown error location"
        frame = tb[-1]
        line_no = frame.lineno
        line_text = frame.line.strip() if frame.line else "(still unavailable)"

        error_message += f"\nError in code block at line {line_no}:"
        error_message += f"\n>>> {line_text}\n{e.__class__.__name__}: {e}"
        raise Exception(error_message)
