#!/usr/bin/env bash
flake8 .
coverage run -m unittest
coverage html
coverage-badge -fo coverage.svg
cp readme_main.md README.md
python -m fcomments -h >> README.md
echo \`\`\` >> README.md
