# PygmenTeX

A Python-based LaTeX package for typesetting code listings using Pygments.

Pygments is a generic syntax highlighter for general use in all kinds of
software such as forum systems, wikis or other applications that need to
prettify source code.

**Requirements:** You need to have Python and Pygments installed. For instructions, please refer to the [Pygments home page](http://pygments.org/).

## The PygmenTeX Difference: Efficiency through Batching

Unlike other packages that call Pygments for *each* code snippet (a slow process), PygmenTeX collects all snippets and processes them in a **single batch**. This can lead to a significant reduction in compilation time for documents with many listings.

## Quick Start

1.  **Installation:** Place the `pygmentex.sty` file in a directory where LaTeX can find it. Ensure the `pygmentex.py` script is executable and located in a directory in your `PATH`.

2.  **Use it in your LaTeX document:**
    ```latex
    \documentclass{article}
    \usepackage{pygmentex} % Uses the 'default' style by default

    \begin{document}

    % Highlight a code snippet
    \begin{pygmented}[lang=c]
    #include <stdio.h>
    int main(void)
    {
       int a, b, c;
       printf("Enter two numbers to add: ");
       scanf("%d%d", &a, &b);
       c = a + b;
       printf("Sum of entered numbers = %d\n", c);
       return 0;
    }
    \end{pygmented}

    % Highlight in line
    In this program, \pyginline[lang=c]|int| is a type and
    \pyginline[lang=c]|"Enter two numbers to add: "| is a literal
    string.

    % Highlight an external file
    \inputpygmented[lang=java, style=monokai]{Factorial.java}

    \end{document}
    ```

3.  **Compile the document with LaTeX (first run):** Snippets are collected into a `.snippets` file.
4.  **Run the Python Script:** Process the snippets with `pygmentex.py` to generate a `.pygmented` file.
    ```bash
    pygmentex.py your_document.snippets
    ```
5.  **Compile the document with LaTeX (second run):** The final document is produced using the pre-formatted output.

> **Note:** Shell escape (`--shell-escape`) is **not required**. The processing is a separate, explicit step. **However, if shell escape is enabled, the `pygmentex.py` script may be executed automatically.**

For full documentation and examples, see [pygmentex-manual.pdf](pygmentex-manual.pdf).

## License

This project is licensed under the LaTeX Project Public License (LPPL), version v1.3c or later.
