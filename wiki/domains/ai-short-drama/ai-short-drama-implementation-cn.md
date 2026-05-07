---
type: workflow
title: "AI 短剧实施手册"
tags: [ai-short-drama, implementation, zh]
---

# AI 短剧实施手册

## 目标

把 Karpathy 的 LLM Wiki 思想用于 AI 短剧：让 LLM 不只是一次性回答“怎么拍”，而是持续维护一个制作知识库。每个项目、镜头、提示词、复盘都能沉淀回来。

## 本仓库结构

```text
raw/                                原始资料和证据
wiki/                               Markdown 知识数据库
wiki/index.md                       人类可读总索引
wiki/log.md                         数据库演化日志
wiki/domains/ai-short-drama/        AI 短剧领域知识
wiki/domains/ai-short-drama/templates/  AI 短剧领域模板
wiki/experts/                       可复用专家思想页
wiki/projects/                      具体项目实践
services/wiki-service/              MCP/API 访问层契约
```

原则：外部服务不要直接依赖这些路径，应该通过 `services/wiki-service/` 定义的 MCP/API 使用 page id 访问 Wiki。

## 第一步：建立项目资料

为每个短剧项目建立一个项目目录，例如：

```text
wiki/projects/project-001/
  brief.md
  references/
  generated/
```

`brief.md` 至少写：

- 题材。
- 目标平台。
- 时长。
- 观众。
- 核心情绪。
- 参考作品。
- 工具链。

## 第二步：让 LLM 建项目 Wiki

让 LLM 基于 brief 生成：

```text
wiki/projects/project-001/project-001-project-overview.md
wiki/projects/project-001/project-001-brief.md
wiki/projects/project-001/project-001-action-plan.md
wiki/projects/project-001/project-001-continuity-bible.md
wiki/projects/project-001/project-001-beat-outline.md
wiki/projects/project-001/project-001-scene-cards.md
wiki/projects/project-001/project-001-shot-list.md
wiki/projects/project-001/project-001-prompt-packs.md
wiki/projects/project-001/project-001-review.md
wiki/projects/project-001/project-001-postmortem.md
```

如果项目目录还不存在，先创建 `wiki/projects/`。

## 第三步：按专家顺序推进

### 编剧专家

输出：

- 一句话钩子。
- 主角目标。
- 阻碍。
- 反转。
- 情绪回报。
- 5-8 个 beat。

### 分镜专家

输出：

- 每个 beat 的镜头拆解。
- 景别。
- 镜头运动。
- 反应镜头。
- 插入镜头。
- 转场建议。

### 连续性专家

输出：

- 人物固定描述。
- 服装和道具。
- 场景规则。
- 时间线。
- 禁止漂移项。

### 提示词专家

输出：

- 角色固定 prompt。
- 场景固定 prompt。
- 单镜头视频 prompt。
- 负面 prompt。
- 失败重试策略。

### 剪辑专家

输出：

- 粗剪顺序。
- 每镜头建议时长。
- 切点。
- 插入镜头位置。
- 字幕节奏。
- 声音桥建议。

### 声音专家

输出：

- 对白/配音方案。
- 音乐 cue。
- 环境声。
- 音效。
- 静音或停顿设计。

## 第四步：生成镜头表

使用 [[shot-list-template|镜头表模板]]。每一行必须能回答：

- 这个镜头为什么存在？
- 它表达哪个剧情信息？
- 它承接哪个镜头？
- 它切向哪个镜头？
- 它需要锁定哪些连续性细节？
- 失败时是重生、替换、遮盖还是删掉？

## 第五步：把复盘写回 Wiki

每次完成一个短剧后，追加：

```text
wiki/projects/project-001/project-001-postmortem.md
```

复盘内容：

- 哪些提示词稳定。
- 哪些镜头最难生成。
- 哪些连续性问题最常见。
- 哪些剪辑策略有效。
- 哪些声音策略提升质感。
- 下一次项目应修改哪些规则。

然后更新：

- [[prompt-expert]]
- [[storyboard-expert]]
- [[editing-expert]]
- [[continuity-expert]]
- `wiki/index.md`
- `wiki/log.md`

## 最小启动命令

你可以直接对 LLM 说：

```text
请为一个 60 秒 AI 短剧项目初始化 Wiki：
题材是 ...
目标平台是 ...
风格是 ...
请依次生成项目概览、人物卡、连续性圣经、beat outline、场景卡、镜头表、提示词包和审片清单。
```

## 质量标准

一个 AI 短剧项目不是素材多就好，而是这些东西一致：

- 故事目标一致。
- 人物外观一致。
- 场景空间一致。
- 镜头逻辑一致。
- 剪辑节奏一致。
- 声音情绪一致。

## 链接

- [[ai-short-drama-cn]]
- [[ai-short-drama-expert-system-cn]]
- [[ai-short-drama-production-workflow]]
- [[review-checklist-template]]
