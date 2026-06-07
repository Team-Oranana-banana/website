import json
import os
import shutil

def get_templates_to_build():
    if not os.path.exists("build.txt"):
        return []

    with open("build.txt", encoding="utf-8") as f:
        return [
            line.strip()
            for line in f
            if line.strip()
        ]
    
def generate_team():
    if not os.path.exists("team"):
        return "<p>No team members found.</p>"

    html = ""

    for filename in sorted(os.listdir("team")):
        if not filename.endswith(".json"):
            continue

        path = os.path.join("team", filename)

        with open(path, encoding="utf-8") as f:
            member = json.load(f)

        name = member.get("name", "Unknown")
        url = member.get("url")
        roles = member.get("roles", "")
        projects = member.get("projects", [])

        if url:
            name_html = f'<a href="{url}">{name}</a>'
        else:
            name_html = name

        projects_html = ""

        for project in projects:
            projects_html += f"<li>{project}</li>\n"

        html += f"""
<details class="member">
    <summary>{name_html}</summary>

    <p>
        {roles}
    </p>

    <details>
        <summary>Working on the following:</summary>

        <ul>
            {projects_html}
        </ul>
    </details>
</details>
"""

    return html

def generate_projects():
    if not os.path.exists("projects"):
        return "<p>No projects found.</p>"

    html = ""

    for filename in sorted(os.listdir("projects")):
        if not filename.endswith(".json"):
            continue

        path = os.path.join("projects", filename)

        with open(path, encoding="utf-8") as f:
            project = json.load(f)

        name = project.get("name", "Unnamed Project")
        description = project.get("description", "")

        html += f"""
<div class="project">
    <strong>{name}</strong>

    <p>
        {description}
    </p>
</div>
"""

    return html

def generate_roadmap():
    if not os.path.exists("roadmap.txt"):
        return "<li>[ ROADMAP EMPTY ]</li>"

    with open("roadmap.txt", encoding="utf-8") as f:
        lines = [line.strip() for line in f if line.strip()]

    if not lines:
        return "<li>[ ROADMAP EMPTY ]</li>"

    return "\n".join(
        f"<li>{line}</li>"
        for line in lines
    )

def generate_status():
    if not os.path.exists("status.txt"):
        return "<p></p>"

    with open("status.txt", encoding="utf-8") as f:
        lines = [line.strip() for line in f if line.strip()]

    if not lines:
        return "<p></p>"

    return "\n".join(
        f"<p>{line}</p>"
        for line in lines
    )

def main():
    os.makedirs("output", exist_ok=True)

    if os.path.exists("template.html"):
        with open("template.html", "r", encoding="utf-8") as f:
            template = f.read()

        compiled = template
        compiled = compiled.replace("{TEAM}", generate_team())
        compiled = compiled.replace("{PROJECTS}", generate_projects())
        compiled = compiled.replace("{ROADMAP}", generate_roadmap())
        compiled = compiled.replace("{STATUS}", generate_status())

        output_file = os.path.join("output", "index.html")
        with open(output_file, "w", encoding="utf-8") as f:
            f.write(compiled)
            
        print(f"Built: {output_file}")
    else:
        print("Missing template file: template.html")

    assets_to_copy = get_templates_to_build()

    for filename in assets_to_copy:
        if not os.path.exists(filename):
            print(f"Missing asset file: {filename}")
            continue

        output_file = os.path.join("output", filename)
        
        output_dir = os.path.dirname(output_file)
        os.makedirs(output_dir, exist_ok=True)

        shutil.copy2(filename, output_file)
        print(f"Copied asset: {output_file}")


if __name__ == "__main__":
    main()