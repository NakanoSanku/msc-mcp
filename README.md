# MSC MCP Server

MCP server for [MSC (Multi‑Screencap Control)](https://github.com/NakanoSanku/msc)，
提供通过 MCP 协议调用 Android 截图/设备信息等能力的后台服务。

> 简单理解：在支持 MCP 的客户端里（例如 Claude 桌面版），
> 可以把这个项目配置成一个本地 MCP Server，然后直接调用
> `list_devices` / `capture_screenshot` 等工具来操作你的 Android 设备。

---

## 功能概览

- `list_devices`：列出当前通过 ADB 连接的 Android 设备。
- `get_device_info`：获取指定设备的型号、SDK 版本、厂商等信息。
- `install_droidcast`：在指定设备上安装 DroidCast，用于高质量投屏截图。
- `capture_screenshot`：从设备截取屏幕图像并以 PNG 形式通过 MCP 返回。
  - 支持的截图方式：`adb`（默认）、`droidcast`、`minicap`、`mumu`。

---

## 环境要求

- Python `>= 3.10`
- 已安装并在 `PATH` 中的 `adb`
- [uv](https://github.com/astral-sh/uv)（用于创建虚拟环境和运行命令）
- 系统可以访问 GitHub 以安装 `msc` 依赖

---

## 安装与开发环境

在项目根目录执行（会自动创建/使用 `.venv` 虚拟环境）：

```bash
uv sync
```

运行单元测试：

```bash
uv run python -m unittest tests.test_main tests.test_server
```

如需运行全部测试：

```bash
uv run python -m unittest
```

---

## 作为 MCP Server 启动

在项目根目录运行：

```bash
uv run python -m msc_mcp
```

或使用脚本入口（安装后）：

```bash
uv run msc-mcp
```

这两种方式都会在标准输入/输出上启动 MCP server，
供支持 MCP 的客户端通过本地进程方式连接。

### MCP 客户端配置示例（伪代码）

以一个典型的 MCP 客户端配置为例，命令大致类似：

```jsonc
{
  "mcpServers": {
    "msc-mcp": {
      "command": "uv",
      "args": ["run", "python", "-m", "msc_mcp"],
      "env": {}
    }
  }
}
```

具体写法请参考你所使用的 MCP 客户端文档。

---

## 项目结构

- `src/msc_mcp/server.py`：MCP 工具实现（截屏、设备信息等）。
- `src/msc_mcp/__main__.py`：命令行/模块入口，启动 MCP server。
- `tests/test_server.py`：针对工具函数的单元测试。
- `tests/test_main.py`：针对入口函数的单元测试。

---

## 贡献与开发

- 新功能/修复请优先补充或更新 `tests/` 下的对应单元测试。
- 保持函数短小、加上合理的类型标注（Python 3.10+）。
- 在提交前确保所有测试通过：

```bash
uv run python -m unittest
```
