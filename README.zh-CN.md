# Easy Wiki

中文 | [English](README.md)

Easy Wiki 是一个由 LLM 协助长期维护的 Markdown 知识库。

它的目标不是收集链接或堆放笔记，而是把合格的原始证据转化成长期可复用、可查询、可被外部应用调用的知识资产。

这个仓库是 Easy Wiki 的核心平台。它不是 Studio 应用，也不是短剧生产应用本身。

## 仓库结构

```text
raw/                    合格的原始证据
wiki/                   Markdown 知识数据库
services/wiki-service/  HTTP/MCP 访问层
services/governance/    执行治理层
docs/                   架构和策略文档
AGENTS.md               后续 agent 的操作规则
```

当前同级消费项目包括：

```text
C:\Code\easy-wiki-studio
```

`easy-wiki-studio` 会调用本仓库里的 wiki、服务层和治理层能力，用于生成短剧生产基础资产。

## 核心概念

- `raw/` 只保存合格、完整、可读的原始材料。
- `wiki/` 保存编译后的知识、专家视角、工作流、模板、领域知识、项目记录、决策和复盘。
- `services/wiki-service/` 通过稳定 page id、搜索、HTTP 和 MCP 暴露 wiki 能力。
- `services/governance/` 帮助外部应用判断每个执行步骤应该使用哪些 source、derived artifact、expert、workflow 和 template。
- 外部消费者应该使用 service 和 governance contract，而不是硬编码本地文件路径。

## 启动 Wiki Service

在仓库根目录执行：

```powershell
python services/wiki-service/api_server.py
```

常用接口：

```text
GET  http://127.0.0.1:8765/health
GET  http://127.0.0.1:8765/pages
GET  http://127.0.0.1:8765/pages/script-expert
GET  http://127.0.0.1:8765/search?q=shot%20unit
GET  http://127.0.0.1:8765/healthcheck
POST http://127.0.0.1:8765/compile-source
POST http://127.0.0.1:8765/compile-missing-sources
POST http://127.0.0.1:8765/projects
```

## 运行测试

```powershell
python -m unittest discover -s tests -p "test_*.py"
```

## 重要文档

- [整体架构](docs/overall-architecture.md)
- [功能边界](docs/function-boundaries.md)
- [治理层](docs/governance-layer.md)
- [Raw 存储策略](docs/raw-storage-policy.md)
- [Wiki Service README](services/wiki-service/README.md)
- [Governance Service README](services/governance/README.md)

## 工作边界

Easy Wiki 提供知识资产和平台契约。具体业务执行由领域应用完成。

例如，短剧生产应用在 `easy-wiki-studio` 中；可复用的专家页、工作流页、访问层和治理层在本仓库中。
