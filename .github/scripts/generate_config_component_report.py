import yaml
from pathlib import Path
import re


def generate_config_summary(config_path: Path) -> str:
    if not config_path.exists():
        return "No config.yaml found"
    data = yaml.safe_load(config_path.read_text())
    lines = ["# Configuration Summary", ""]
    for section, values in data.items():
        lines.append(f"## {section}")
        if isinstance(values, dict):
            for key, value in values.items():
                lines.append(f"- **{key}**: {value}")
        else:
            lines.append(str(values))
        lines.append("")
    return "\n".join(lines)


def analyze_components(components_dir: Path) -> str:
    if not components_dir.is_dir():
        return "No components directory"
    lines = ["# Components Report", ""]
    for file in sorted(components_dir.glob("*.py")):
        text = file.read_text()
        class_count = len(re.findall(r"^class ", text, flags=re.MULTILINE))
        func_count = len(re.findall(r"^def ", text, flags=re.MULTILINE))
        lines.append(f"- **{file.name}**: {class_count} classes, {func_count} functions")
    return "\n".join(lines)


def main():
    report_dir = Path(".github/reports")
    report_dir.mkdir(parents=True, exist_ok=True)
    config_summary = generate_config_summary(Path("config.yaml"))
    component_summary = analyze_components(Path("components"))
    report = "\n\n".join([config_summary, component_summary])
    output_file = report_dir / "config_component_report.md"
    output_file.write_text(report)
    print(f"Report written to {output_file}")


if __name__ == "__main__":
    main()
