import os
import typer
from jinja2 import Environment, FileSystemLoader

## Begin to create from jinja template file
def generate_template(module_name: str, module_version: str, s3_name: str, environment_name: str, backend_name: str):
    """Generate Terraform module from template."""
    ## Check Environment path 
    template_env =  Environment(loader=FileSystemLoader('.'))

    ## Call template file
    template_file = template_env.get_template('s3-tfstate-template.j2')

    ## Parse Data
    data = {
        "module_name": module_name,
        "module_version": module_version,
        "s3_name": s3_name,
        "environment_name": environment_name,
        "backend_name": backend_name,
    }

    os.makedirs("backend/", exist_ok=True)
    output_file = "backend/"+backend_name+".tf"

    ## Render template
    rendered_template = template_file.render(data)
    ## Write to terraform file
    with open(output_file, 'w') as w_f:
        w_f.write(rendered_template)

    print(f"Terraform file is written to: {output_file}")

if __name__ == "__main__":
    typer.run(generate_template)