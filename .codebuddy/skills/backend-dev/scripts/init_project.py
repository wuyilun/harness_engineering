#!/usr/bin/env python3
"""后端项目初始化脚本 - 创建 FastAPI 项目骨架"""

import os
import sys

def create_project(base_dir: str) -> None:
    dirs = [
        f"{base_dir}/app",
        f"{base_dir}/app/models",
        f"{base_dir}/app/schemas",
        f"{base_dir}/app/api/v1",
        f"{base_dir}/app/services",
        f"{base_dir}/app/repositories",
        f"{base_dir}/app/middleware",
        f"{base_dir}/alembic/versions",
        f"{base_dir}/tests",
        f"{base_dir}/tests/unit",
        f"{base_dir}/tests/integration",
        f"{base_dir}/tests/api",
    ]

    for d in dirs:
        os.makedirs(d, exist_ok=True)

    # Create __init__.py files
    init_dirs = [
        f"{base_dir}/app",
        f"{base_dir}/app/models",
        f"{base_dir}/app/schemas",
        f"{base_dir}/app/api",
        f"{base_dir}/app/api/v1",
        f"{base_dir}/app/services",
        f"{base_dir}/app/repositories",
        f"{base_dir}/app/middleware",
    ]

    for d in init_dirs:
        init_file = os.path.join(d, "__init__.py")
        if not os.path.exists(init_file):
            with open(init_file, "w") as f:
                f.write("")

    print(f"Project skeleton created at {base_dir}")


if __name__ == "__main__":
    target = sys.argv[1] if len(sys.argv) > 1 else "src/backend"
    create_project(target)
