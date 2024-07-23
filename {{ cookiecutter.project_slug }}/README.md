# {{ cookiecutter.project_name }}

## Getting Started

Create a new environment
```bash
conda create -n {{ cookiecutter.project_slug }} python={{ cookiecutter.default_python }}
conda activate {{ cookiecutter.default_python }}
pip install -e .
```
