---
type: log
updated: 2026-05-06
---

# Log

## [2026-05-04] implementation | Number Rule Runner 固定规则判断行

实现 Rule Row 机制，把数学判断从“按当前值心算”改为“看固定规则选唯一正确数字门”。

修正：

- Rule Row 横排从“三个答案门”改为 `[左答案] [中间规则牌] [右答案]`。
- 中间规则牌不是答案，触碰会扣分并打断 combo。
- 左右答案门严格只有一个正确答案。
- 修复部分早期教学行和低难度行只有 1-2 个形状、存在空 lane 的问题，现在每一横排都填满左中右 3 个对象。
- 规则牌视觉改为中间警示横牌，显示 `PICK ...`，并把 `x3` 改为 `3-MULT` 避免误解成乘法门。

新增：

- 海外解压小游戏换题-rule-row机制

更新：

- `apps/Number Rule Runner/js/core/generator.js` 增加 `quiz` 行生成、规则轮换和阶段化奖惩。
- `apps/Number Rule Runner/js/core/game.js` 增加 `applyQuiz()`、`quiz` 类型和规则预告。
- `apps/Number Rule Runner/index.html`、`styles.css`、`js/app.js`、`js/render/canvas.js` 增加 HUD 与 Canvas 显示。
- `apps/Number Rule Runner/test.html` 增加唯一答案、首分钟出现和 10 分钟路线测试。
- `apps/Number Rule Runner/README.md` 增加 Rule Row 范围说明。

验证：

- Chrome headless 打开 `test.html`，显示 `ALL_TESTS_PASSED`。
- Chrome headless 重新生成 390x844 移动预览截图成功，并调整 Tune 按钮避免 HUD 重叠。

## [2026-05-04] mechanic | Number Rule Runner 属性皮肤成长

新增快速局外成长，让玩家前几局就能解锁视觉变化。

新增：

- 海外解压小游戏换题-属性皮肤成长
- `apps/Number Rule Runner/js/data/skins.js`

实现：

- 定义 Speed、Power、Guard、Focus、Control、Danger 等属性颜色体系。
- 8 个可解锁皮肤只改变球体视觉，不改变数值能力。
- 存活 15 秒、5 combo、拾取 Shield、答对 Rule Row、命中 Target、触发 Fever、低值存活和 60 秒生存会即时解锁皮肤。
- 解锁后自动切换当前皮肤，并用浮字反馈。
- 开始页增加 `Skin` 按钮，可循环选择已解锁皮肤。
- 皮肤成长改为本局临时成长，失败后重置回 `Classic Blue`。

验证：

- Chrome headless 打开 `test.html`，显示 `ALL_TESTS_PASSED`。
- Chrome headless 重新生成 390x844 移动预览截图成功。

## [2026-05-04] mechanic | Number Rule Runner Album 拼图成长

新增永久局外成长：失败后皮肤重置，但 Outfit 拼图进度保留。

新增：

- 海外解压小游戏换题-album拼图成长
- `apps/Number Rule Runner/js/data/album.js`

实现：

- 一张 Outfit 图拆成 6 块碎片。
- 存活 15 秒、30 秒、5 combo、3 次 Rule Row 正确、2 次 Target、1 次 Fever 各给一块碎片。
- 每局同一条件只给一次碎片。
- 完成整张图后永久解锁视觉特效，并自动进入下一张图。
- 首批特效包括青蓝拖尾、专注十字光、金色外环和爆发星形光。
- 开始页显示当前 Album 进度。

验证：

- Chrome headless 打开 `test.html`，显示 `ALL_TESTS_PASSED`。

## [2026-05-04] visual | Number Rule Runner 颜色语义区分

根据颜色专家视角整理危险系和加成系颜色，避免扣分、警告、奖励和成长反馈混在一起。

更新：

- 危险 / 扣分统一使用红和洋红：`#ff174f`、`#ff385c`。
- 警告 / 别碰统一使用橙色：`#ff8a3d`、`#ff9f1c`、`#ff5a36`。
- 正收益统一使用绿色：`#35f08f`。
- 奖励 / 完成 / Album 统一使用金色：`#ffd447`。
- Rule 正确 / Focus 统一使用青绿：`#39f5c9`。
- Shield 统一使用青蓝：`#5bd8ff`。
- Power / Fever 统一使用紫色：`#9d6cff`、`#c79cff`。
- 同步更新 Canvas、HUD、路线预告、皮肤目录和 README 说明。

验证：

- `test.html` 增加关键皮肤语义色断言。

## [2026-05-04] feel | Number Rule Runner 通道间隔优化

用户反馈通道间隔设计不好，修正视觉通道和碰撞判定。

更新：

- 赛道从细线分隔改为半透明 lane band 加虚线 gutter，左中右通道边界更清楚。
- 移动端 lane 间距从 `min(112, width * 0.28)` 调整为 `min(128, max(96, width * 0.31))`。
- 碰撞判定从统一偏宽改为按类型收窄：普通门、规则牌、尖刺和路障不同宽度。
- 规则牌和路障判定更窄，减少站在相邻通道却误撞中间牌的感觉。
- `test.html` 增加通道碰撞宽度断言。

验证：

- Chrome headless 打开 `test.html`，显示 `ALL_TESTS_PASSED`。
- Chrome headless 重新生成 390x844 移动预览截图成功。

## [2026-05-04] fix | Number Rule Runner 修复穿越横排不死亡

用户反馈可以从通道缝隙穿越横排不触发失败或惩罚。

修复：

- 碰撞从“单个门重叠才触发”改为“横排到达时按最近通道结算”。
- 一横排被结算后，左中右三个对象一起消耗，避免同排重复触发。
- 即使玩家站在两条通道之间，也会命中最近 lane 的门，不能从门缝穿过。
- Canvas 为障碍横排增加虚线连接，让玩家理解这是一整排决策。
- `test.html` 增加 gutter 位置不能穿越、横排一次性消耗的断言。

验证：

- Chrome headless 打开 `test.html`，显示 `ALL_TESTS_PASSED`。
- Chrome headless 重新生成 390x844 移动预览截图成功。

## [2026-05-04] feel | Number Rule Runner 横排错位布局

用户反馈一横的位置不应该固定。

更新：

- 同一个决策组保留 `rowId` 和 `rowZ`，但每个 lane 根据 `laneZOffset()` 获得轻微前后错位。
- 预览距离仍按决策组中心 `rowZ` 显示，避免 HUD 被最前面的单个门扰动。
- 碰撞结算改为先按当前玩家位置选最近 lane，再等该 lane 的错位门到达时结算整组。
- Canvas 横排连接线改为跟随三个错位点折线连接，而不是固定水平线。
- `test.html` 增加错位生成和预览 / 横排结算相关覆盖。

验证：

- Chrome headless 打开 `test.html`，显示 `ALL_TESTS_PASSED`。
- Chrome headless 重新生成 390x844 移动预览截图成功。

## [2026-05-04] fix | Number Rule Runner 通道分界卡缝惩罚

用户反馈仍然可以卡在两个 lane 中间无伤。

修复：

- 两条 lane 之间定义为 orange danger gutter，而不是可安全站位区域。
- 玩家在 gutter 内遇到决策组时触发 `SCRAPE -N`，并消耗整组。
- 正常 lane 中心仍然按对应 lane 的门结算。
- Canvas 将 gutter 画成橙色危险带和虚线，给玩家明确视觉提示。
- `test.html` 增加 gutter 检测、卡缝扣分、lane 中心正常结算测试。

验证：

- Chrome headless 打开 `test.html`，显示 `ALL_TESTS_PASSED`。
- Chrome headless 重新生成 390x844 移动预览截图成功。

## [2026-05-04] content | Number Rule Runner 扩展 Album 页数

用户反馈 Album 只有 4 页，长期目标不足。

更新：

- Album 从 4 张 Outfit 扩展到 10 张 Outfit。
- 新增 `Guard Armor`、`Danger Suit`、`Grip Sneakers`、`Arcade Visor`、`Space Coat`、`Crown Outfit`。
- 新增永久特效：`Shield Halo`、`Danger Pulse Field`、`Grip Sparks`、`Prism Orbit`、`Comet Tail`、`Crown Rays`。
- Canvas 增加对应特效绘制。
- `test.html` 验证全部扩展页都能完成，并且最后一页解锁 `Crown Rays`。

验证：

- Chrome headless 打开 `test.html`，显示 `ALL_TESTS_PASSED`。

## [2026-05-02] structure | Initialize Easy Wiki

Created the initial LLM Wiki structure:

- `AGENTS.md`
- `raw/`
- `wiki/`
- `wiki/index.md`
- `wiki/log.md`

Initialized the first knowledge domain: [[ai-short-drama|AI Short Drama]].

## [2026-05-02] source | Karpathy LLM Wiki

Registered root file `llm-wiki.md` as the seed reference and created [[karpathy-llm-wiki资料|Karpathy - LLM Wiki]] plus [[llm-wiki-pattern|LLM Wiki Pattern]] and [[llm-wiki-vs-rag|LLM Wiki vs RAG]].

## [2026-05-02] topic | AI Short Drama Chinese Wiki

Added Chinese entry pages for AI short drama:

- [[ai-short-drama-cn|AI 短剧知识地图]]
- [[ai-short-drama-expert-system-cn|AI 短剧专家系统]]
- [[ai-short-drama-implementation-cn|AI 短剧实施手册]]

## [2026-05-02] ingest | AI Short Drama Expert Research Batch 1

Searched and registered the first external expert-source batch for AI short drama production. Created:

- `raw/expert-research-2026-05-02.md`
- [[pixar故事与电影语法]]
- [[walter-murch-六法则]]
- [[youtube观众留存]]
- [[randy-thom-为声音设计电影]]
- [[dga导演创作访谈]]
- [[ai视频提示词指南]]

Next action: propagate the strongest source ideas into expert pages and templates.

## [2026-05-02] synthesize | Expert Pages Updated From Research Batch 1

Propagated source ideas into:

- [[storyboard-expert]]
- [[editing-expert]]
- [[sound-expert]]
- [[director-expert]]
- [[prompt-expert]]
- [[script-expert]]
- [[cinematography-expert]]
- [[continuity-expert]]

Key synthesis:

- Pixar/Khan reinforces storyboard/storyreel iteration and visual grammar.
- Murch gives editing priority: emotion and story before spatial continuity.
- YouTube retention reports become post-release pacing diagnostics.
- Randy Thom moves sound design earlier into story and scene planning.
- DGA interviews reinforce director ownership of motivation, staging, and whole-story coherence.
- Sora/Runway guides reinforce shot-level prompting with camera, motion, lighting, and temporal progression.

## [2026-05-02] workflow | New Domain Expert Research Workflow

Added [[new-domain-expert-research-workflow]] to formalize the user's preferred process:

1. Decompose a new domain into expert roles.
2. Search expert sources role by role.
3. Ingest sources into the wiki.
4. Synthesize expert frameworks and templates.
5. Plan execution.
6. Start actual work.
7. Postmortem and update the wiki.

Added [[ai-short-drama-expert-map]] as the AI short drama-specific expert decomposition and search map.

## [2026-05-03] structure | Add Domain And Project Layers

Added long-term structure for durable knowledge and concrete execution:

- [[domain-index]]
- [[ai-short-drama-domain-overview]]
- [[ai-short-drama-domain-sources]]
- [[ai-short-drama-domain-framework]]
- [[ai-short-drama-domain-workflows]]
- [[ai-short-drama-domain-projects]]
- [[ai-short-drama-domain-open-questions]]
- [[project-index]]
- [[project-start-workflow]]
- [[decision-index]]
- [[postmortem-index]]

Added project templates:

- [[project-overview-template]]
- [[project-brief-template]]
- [[project-action-plan-template]]
- [[project-decisions-template]]
- [[project-working-notes-template]]
- [[project-postmortem-template]]

## [2026-05-03] architecture | Wiki Database And MCP/API Access Layer

Adjusted the repository architecture around the user's long-term direction:

- `wiki/` is the markdown knowledge database.
- `services/wiki-service/` is the future MCP/API access layer.
- External services should use page ids and service calls instead of hard-coded file paths.
- Added `docs/core-knowledge-architecture.md`.
- Added service contract docs under `services/wiki-service/`.
- Added a minimal read-only HTTP API implementation:
  - `services/wiki-service/wiki_core.py`
  - `services/wiki-service/api_server.py`
- Moved AI short drama topic pages, domain-specific workflows, and domain-specific templates under `wiki/domains/ai-short-drama/`.
- Removed empty legacy `wiki/topics/` and `wiki/templates/` directories.
- Runtime verification was not completed because Python is not installed in the current shell environment.

## [2026-05-03] architecture | Function Boundaries

Added `docs/function-boundaries.md` to clarify current responsibilities, non-goals, boundary risks, and maturity state.

Updated `AGENTS.md` to remove `topic` as an active top-level page type. Existing `type: topic` pages are now treated as domain entry pages under domain folders.

## [2026-05-03] raw | Source Packet Upgrade

Upgraded the raw evidence layer from a link-only registry toward source packets:

- Added `raw/sources/README.md`.
- Added `raw/sources/_templates/source-packet-template.md`.
- Added first-pass source packets, later migrated to `raw/sources/<source-id>/`.
- Split the first expert research batch into 10 raw source packets.

Current status: these packets are still partly `link-only` / `needs-capture`, but each source now has explicit metadata, acquisition status, rights notes, role coverage, and a related wiki source page. Future ingest should add local originals, transcripts, user notes, or mark sources as restricted.

## [2026-05-03] raw | Download Core Expert Source Files

Downloaded public HTML snapshots for sources that allowed direct capture:

- `raw/sources/pixar-in-a-box/captures/original.html`
- `raw/sources/walter-murch-rule-of-six/captures/original.html`
- `raw/sources/walter-murch-rule-of-six/captures/supporting-original.html`
- `raw/sources/randy-thom-designing-for-sound/captures/original.html`

Capture was blocked or incomplete for several sources and recorded accurately:

- Pixar/Khan storytelling: JavaScript shell only, marked `needs-capture`.
- YouTube audience retention: timeout, marked `needs-capture`.
- DGA interview: Incapsula challenge, marked `restricted`.
- OpenAI Sora help: JavaScript/refresh page, marked `needs-capture`.
- OpenAI video generation API: Cloudflare challenge, marked `needs-capture`.
- Runway guides: Cloudflare challenge, marked `restricted`.

## [2026-05-03] raw | Redesign Source Storage

Redesigned `raw/` from batch-owned source folders to source-centric packets:

- `raw/sources/<source-id>/source.md`
- `raw/sources/<source-id>/captures/`
- `raw/sources/<source-id>/assets/`
- `raw/sources/<source-id>/notes/`

Moved research batch files and capture logs into `raw/batches/`. Batches now index source ids instead of owning source folders.

## [2026-05-03] raw | Simplify Raw To Complete Originals Only

Simplified `raw/` after user feedback:

- `raw/` now stores complete original files only.
- Kept valid originals under `raw/`.
- Moved source cards, capture logs, notes, blocked pages, and failed captures to `docs/capture-attempts/`.
- Updated source pages to point to `raw/...` where a valid local original exists.

Raw originals at that point were later converted to readable Markdown:

- `raw/karpathy-llm-wiki-原文.md`
- `docs/capture-attempts/html-snapshots/wechat-llm-wiki-content-3.html`
- `docs/capture-attempts/html-snapshots/pixar-in-a-box.html`
- `docs/capture-attempts/html-snapshots/walter-murch-rule-of-six.html`
- `docs/capture-attempts/html-snapshots/walter-murch-rule-of-six-supporting.html`
- `docs/capture-attempts/html-snapshots/randy-thom-designing-for-sound.html`

Added `docs/raw-storage-policy.md` as the active raw-layer policy.

## [2026-05-03] ingest | WeChat LLM Wiki Content 3.0 Case Study

Captured and ingested the WeChat article "一篇文章卖了20万，开源CC+Obsidian打造的LLM Wiki 内容创作3.0系统".

Created:

- `raw/sources/wechat-uSNIibUFNVnZg1JSoeqtHg/`
- [[微信-llm-wiki内容创作3系统]]
- [[knowledge-compile-pipeline]]

Updated:

- [[llm-wiki-pattern]]
- `wiki/index.md`

Borrowed ideas:

- Compile pipeline should go beyond summary.
- Track source utilization.
- Add stronger health-check dimensions.
- Treat instruction files as operational infrastructure.

## [2026-05-03] raw | Convert Raw Originals To Readable Articles

Tightened the raw layer after user feedback that `raw/` should not contain HTML files.

- Moved HTML snapshots from `raw/` to `docs/capture-attempts/html-snapshots/`.
- Kept only readable Markdown originals under `raw/`.
- Cleaned obvious navigation/footer chrome from the Walter Murch, Randy Thom, and Pixar Markdown originals.
- Updated source pages to point to `.md` raw originals.
- Updated raw storage policy, architecture notes, AGENTS rules, and service write policy to disallow HTML snapshots/webpage wrappers in `raw/`.

Current raw originals:

- `raw/karpathy-llm-wiki-原文.md`
- `raw/微信-llm-wiki内容创作3系统-原文.md`
- `raw/pixar-in-a-box.md`
- `raw/walter-murch-六法则-原文.md`
- `raw/walter-murch-六法则-补充原文.md`
- `raw/randy-thom-为声音设计电影-原文.md`

Note: `pixar-in-a-box.md` is the complete readable Pixar landing-page text, not a full Khan Academy lesson transcript. It should be replaced or supplemented when a full lesson transcript is captured.

## [2026-05-03] raw | Flatten Raw Directory

Flattened `raw/` after user feedback that it should not contain nested source directories.

- Moved readable originals from `raw/originals/` to `raw/`.
- Removed empty `raw/originals/` and `raw/articles/` directories.
- Updated source pages, raw storage policy, AGENTS rules, service write policy, and workflow examples to use flat `raw/<source-id>.md` paths.

Current raw files:

- `raw/karpathy-llm-wiki-原文.md`
- `raw/微信-llm-wiki内容创作3系统-原文.md`
- `raw/pixar-in-a-box.md`
- `raw/walter-murch-六法则-原文.md`
- `raw/walter-murch-六法则-补充原文.md`
- `raw/randy-thom-为声音设计电影-原文.md`

## [2026-05-03] service | Implement Compile And Health Workflows

Implemented the first executable service layer for the WeChat LLM Wiki 3.0-style workflow.

Added to `services/wiki-service/`:

- `compile_source()` and `POST /compile-source` / `POST /ingest`
- `source_usage()` and `GET /sources/usage`
- `health_check()` and `GET /healthcheck`
- `create_project()` and `POST /projects`
- Improved frontmatter parsing for multiline `raw_original_paths`

Added [[source-compile-workflow]] and updated [[knowledge-compile-pipeline]], `AGENTS.md`, service API docs, MCP tool docs, storage contract, and function-boundary docs.

Important boundary: service compile creates source-page drafts and reports next actions. Durable synthesis into expert, concept, domain, workflow, and template pages should still be reviewed by an LLM maintainer instead of being mechanically promoted.

Runtime verification is still blocked until a real Python 3 interpreter is installed; this shell resolves `python` to the Windows Store placeholder.

## [2026-05-03] docs | Add Overall Architecture Document

Added `docs/overall-architecture.md` as the top-level architecture explanation for the repository.

It documents:

- Overall positioning.
- Layer responsibilities.
- Knowledge compile flow.
- Source usage and health checks.
- Domain and project model.
- AI short drama knowledge model.
- MCP/API access model.
- Current maturity and near-term roadmap.

Updated `wiki/index.md` to include the new architecture document.

## [2026-05-03] docs | Translate Overall Architecture To Chinese

Rewrote `docs/overall-architecture.md` in Chinese while preserving the same architecture content and boundaries.

## [2026-05-03] research | Mini Program Game Expert Sources

Started a new domain bootstrap for building a simple mini program game.

Created:

- mini-program-game-domain-overview
- mini-program-game-expert-map
- mini-program-game-domain-sources
- 微信小游戏官方文档
- cocos发布到微信小游戏
- mdn-canvas教程
- mdn-canvas基础动画
- raph-koster-乐趣原子理论
- jesse-schell-游戏设计艺术
- 腾讯广告小游戏商业化

Updated `wiki/index.md`.

Current synthesis: first build should stay to one screen, one input, one fail condition, one score, and one restart loop. Monetization, social ranking, and complex platform features should be deferred until the core loop works.

## [2026-05-03] raw | Capture Mini Program Game Source Originals

Captured readable local raw files for the initial mini program game source set:

- `raw/wechat-minigame-official-docs.md`
- `raw/cocos发布到微信小游戏-原文.md`
- `raw/mdn-canvas教程-原文.md`
- `raw/mdn-canvas基础动画-原文.md`
- `raw/raph-koster-乐趣原子理论-原文.md`
- `raw/schell-art-of-game-design.md`
- `raw/tencent-ads-minigame-monetization.md`

Updated related `wiki/sources/` pages from `link-only` to local-copy statuses where appropriate.

Quality notes:

- WeChat official docs capture is an index/navigation page; capture exact official chapters later when needed.
- Schell source is a public landing page, not the full book.
- Tencent Ads source is secondary and should not govern platform compliance.

## [2026-05-03] raw | Tighten Raw Entry Criteria

Tightened the raw evidence policy after user feedback that not every captured page should enter `raw/`.

Removed weak local raw files:

- `raw/wechat-minigame-official-docs.md` - official index/navigation page, not a chapter source.
- `raw/schell-art-of-game-design.md` - public landing page, not full source text.
- `raw/tencent-ads-minigame-monetization.md` - weak secondary monetization article.
- `raw/pixar-in-a-box.md` - landing page, not full Pixar/Khan lesson content.

Updated related source pages to link-only weak statuses and added explicit source quality / evidence strength fields.

Updated raw policy docs and agent rules: `raw/` is a qualified evidence store, not a download cache. Landing pages, documentation indexes, and weak secondary pages should remain as `wiki/sources/` link records until stronger originals are captured.

## [2026-05-03] workflow | Add New Domain Research Gate

Updated [[new-domain-expert-research-workflow]] so new domains must start with exploration, research planning, expert decomposition, source search, source candidate review, and archive reminders before execution.

Added [[source-candidate-template]] for classifying search results by source quality, evidence strength, and archive recommendation.

Updated `AGENTS.md`, `docs/raw-storage-policy.md`, and `wiki/index.md`.

## [2026-05-03] workflow | Add Universal Requirement Intake

Added [[requirement-intake-workflow]] as the universal precondition for new domains, projects, source search, source archive, implementation, and architecture changes.

Updated [[new-domain-expert-research-workflow]], [[project-start-workflow]], `AGENTS.md`, `docs/overall-architecture.md`, and `wiki/index.md`.

Core rule: requirements must be clear before exploration, planning, search, archive, project creation, or implementation.

## [2026-05-03] project | 启动抖音小应用 MVP 需求入口

通过需求收集和官方资料分类，启动抖音小应用项目入口。

新增可复用的新领域实施方法论：

- implementation-domain-overview
- implementation-expert-map
- implementation-domain-sources
- [[domain-to-project-implementation-workflow]]
- [[implementation-plan-template]]
- [[mvp-validation-template]]

新增抖音小程序 / 小游戏领域：

- 抖音小程序小游戏-领域总览
- 抖音小程序小游戏-专家地图
- 抖音小程序小游戏-资料地图

新增抖音官方资料候选：

- 抖音开放平台-小程序框架概述
- 抖音开放平台-小程序开发准备
- 抖音开放平台-开发者工具概述
- 抖音开放平台-使用ai开发小程序
- 抖音开放平台-typescript支持

创建第一个项目工作区：

- 抖音小应用mvp-项目总览
- 抖音小应用mvp-需求简报
- 抖音小应用mvp-行动计划
- 抖音小应用mvp-决策记录
- 抖音小应用mvp-工作记录
- 抖音小应用mvp-评审
- 抖音小应用mvp-复盘

当前状态：此通用入口已进一步收敛到具体的西游抽卡小游戏项目。下一步围绕具体小游戏执行。

## [2026-05-03] project | 定义抖音西游抽卡小游戏

用户明确产品方向：

- 解压小游戏.
- 抽卡游戏.
- 西游记角色.
- 角色有属性.
- 抽卡结果可以是角色卡，也可以是属性增值卡.

创建具体活跃项目：

- 抖音西游抽卡小游戏-项目总览
- 抖音西游抽卡小游戏-需求简报
- 抖音西游抽卡小游戏-玩法设计
- 抖音西游抽卡小游戏-卡牌系统
- 抖音西游抽卡小游戏-行动计划
- 抖音西游抽卡小游戏-决策记录
- 抖音西游抽卡小游戏-工作记录
- 抖音西游抽卡小游戏-评审
- 抖音西游抽卡小游戏-复盘

新增抖音小游戏官方资料候选：

- 抖音开放平台-小游戏文档入口
- 抖音开放平台-了解抖音小游戏
- 抖音开放平台-小游戏开发指南
- 抖音开放平台-开发小游戏

当前 MVP 方向：单屏无引擎 Canvas 小游戏，包含点击抽卡、角色卡、属性增值卡、简单本地状态，并先在抖音开发者工具中预览。

## [2026-05-03] docs | 中文化抖音小游戏项目文档

按用户要求，将抖音西游抽卡小游戏相关文档改为中文正文，保持英文文件名和页面 id 不变，方便 MCP/API 稳定引用。

已中文化：

- 抖音西游抽卡小游戏-项目总览
- 抖音西游抽卡小游戏-需求简报
- 抖音西游抽卡小游戏-玩法设计
- 抖音西游抽卡小游戏-卡牌系统
- 抖音西游抽卡小游戏-行动计划
- 抖音西游抽卡小游戏-决策记录
- 抖音西游抽卡小游戏-工作记录
- 抖音西游抽卡小游戏-评审
- 抖音西游抽卡小游戏-复盘
- 抖音小程序小游戏-领域总览
- 抖音小程序小游戏-专家地图
- 抖音小程序小游戏-资料地图
- 抖音小程序 / 小游戏相关 `wiki/sources/` 资料候选页。

## [2026-05-03] planning | 细化抖音西游抽卡小游戏 MVP 规划

继续规划抖音西游抽卡小游戏，新增：

- 抖音西游抽卡小游戏-版本路线
- 抖音西游抽卡小游戏-mvp规格
- 抖音西游抽卡小游戏-界面流程
- 抖音西游抽卡小游戏-技术方案
- 抖音西游抽卡小游戏-试玩验证计划

默认 v0 方案：

- 无引擎 Canvas。
- 无限免费抽。
- 属性卡先加全队。
- 占位图形和文字先验证核心循环。

下一步：创建最小抖音小游戏脚手架，并实现抽卡数据、概率、主界面和基础反馈。

## [2026-05-03] structure | 中文化规划页、资料页和原文文件命名

按用户要求，将人看的文件名改为中文，便于在编辑器侧边栏阅读。

调整范围：

- 抖音西游抽卡小游戏项目规划页。
- 抖音小应用 MVP 入口页。
- 抖音小程序 / 小游戏领域页。
- `wiki/sources/` 资料页。
- `raw/` 原文文件。

处理原则：

- 页面文件名和 wiki 页面 id 改为中文。
- frontmatter 中的机器标识保持稳定，例如 `project: douyin-xiyou-gacha-game`。
- 批量更新所有 Obsidian 双链和 raw 路径引用。
- 更新 `AGENTS.md`，以后中文工作流中的规划页、资料页和原文文件优先使用中文命名。

## [2026-05-03] workflow | 增加需求确认门

根据用户反馈，修正需求理解流程：不能只由 agent 推断默认方案后直接进入规划或实现。

更新：

- `AGENTS.md`
- [[requirement-intake-workflow]]
- 抖音西游抽卡小游戏-项目总览
- 抖音西游抽卡小游戏-行动计划

新增：

- 抖音西游抽卡小游戏-需求确认

新规则：

- 新产品、游戏、应用、工作流或版本计划必须先形成一个命名的需求版本。
- 需求版本要列出包含范围、排除范围、默认假设和未决问题。
- 必须等待用户明确确认，或用户明确授权按当前假设推进。
- 当前西游抽卡小游戏状态调整为“等待用户确认 v0 需求版本”，确认前不开始代码脚手架。

## [2026-05-03] workflow | 明确需求阶段是人类反复推敲区

根据用户进一步说明，修正确认门语义：

- 需要反复推敲确认的是需求阶段。
- 用户确认需求版本后，专家拆分、资料搜索、规划、实现、验证可以按专家流程推进。
- 后续只有在发现改变需求、出现重大取舍或需要用户拥有决策时，才重新回到需求确认。

更新：

- `AGENTS.md`
- [[requirement-intake-workflow]]
- 抖音西游抽卡小游戏-需求确认
- 抖音西游抽卡小游戏-行动计划

## [2026-05-03] project | 确认抖音西游抽卡小游戏 v0 需求

用户确认“先按这个方向继续”。

确认后的 v0 方向：

- 抖音小游戏。
- 西游记主题。
- 解压抽卡。
- 角色卡 + 属性增值卡。
- 无引擎 Canvas。
- 无限免费抽。
- 属性卡先加全队。
- 占位图形和文字先验证核心循环。

更新：

- 抖音西游抽卡小游戏-需求确认
- 抖音西游抽卡小游戏-项目总览
- 抖音西游抽卡小游戏-行动计划
- 抖音西游抽卡小游戏-决策记录
- 抖音西游抽卡小游戏-工作记录

下一步：进入专家流程，绑定关键官方资料和专家视角，然后创建最小抖音小游戏脚手架。

## [2026-05-03] planning | 绑定抖音西游抽卡小游戏专家执行流程

新增：

- 抖音西游抽卡小游戏-专家执行绑定

作用：

- 明确 v0 需求确认后使用哪些专家视角。
- 明确哪些事项可以自动推进。
- 明确哪些变化必须回到 抖音西游抽卡小游戏-需求确认。

## [2026-05-03] implementation | 实现抖音西游抽卡小游戏 v0

创建完整 v0 项目：

- `apps/抖音西游抽卡小游戏/`

实现：

- 抖音小游戏入口和配置。
- 浏览器试玩页。
- 浏览器逻辑测试页。
- 无引擎 Canvas 单屏界面。
- 角色卡池、属性卡池、概率表。
- 抽卡逻辑、重复角色魂魄、属性提升。
- 本地状态保存。
- 抽一次、十连测试、重置。

测试：

- JSON 校验通过。
- 文件引用校验通过。
- 卡池数量和概率权重校验通过。
- Chrome 无头截图验证 `preview.html` 可渲染。
- Chrome 浏览器逻辑测试 `test.html` 通过并显示 `ALL_TESTS_PASSED`。

限制：

- 当前环境无 Node/npm。
- 抖音开发者工具和真机预览需要用户本机验证。

## [2026-05-03] synthesize | 反哺抖音小游戏领域经验

从 抖音西游抽卡小游戏-项目总览 提炼可复用经验，新增：

- 抖音小游戏-最小canvas项目模式
- 抖音小游戏-浏览器预览测试模式

更新：

- 抖音小程序小游戏-领域总览
- 抖音小程序小游戏-专家地图
- `wiki/index.md`

关键结论：

- 项目代码应放在 `apps/`，wiki 保留知识、决策、评审和复盘。
- v0 小游戏可以先用无引擎 Canvas 验证核心循环。
- 浏览器预览和逻辑测试能提高早期验证速度，但不能替代抖音开发者工具和真机预览。

## [2026-05-03] architecture | 规划 Wiki 与应用轻耦合改造

新增：

- `docs/wiki-app-loose-coupling-plan.md`

结论：

- 当前轻耦合方向正确：`wiki/` 存知识，`apps/` 存实现，`services/wiki-service/` 做访问层。
- 当前不足是 wiki 和 apps 之间仍靠人工连接，项目状态、需求版本、测试结果和 app 清单缺少机器可读结构。
- 下一步建议先做 Phase 1：增加 app manifest、apps 总清单，并把 app 与 wiki 项目通过 page id 连接起来。

## [2026-05-03] domain | 增加抖音发布版本检查清单

根据官方文档补充抖音小程序 / 小游戏发布和版本号知识。

新增：

- 抖音小程序小游戏-发布版本检查清单

结论：

- 抖音小程序 / 小游戏可以发布，需要开发者工具上传、开放平台体验测试、提交审核和发布。
- 上传版本需要版本号，小程序上传版本需符合 semver 且高于线上版本；小游戏重新提审版本号也需要递增。
- 当前西游抽卡 v0 还不能直接发布，因为仍是浏览器测试版，未完成 AppID、抖音开发者工具、真机预览、测试按钮清理和提审自查。

## [2026-05-03] domain | 增加海外免费解压小游戏路线评估

新增：

- 海外免费解压小游戏路线评估

结论：

- 海外路线可以绕开国内网络游戏版号高门槛，但仍有平台准入、隐私、年龄分级、抽卡概率、支付/广告和外部引流规则。
- 当前最现实路线是先做免费 Web/PWA 解压抽卡，不收费、不登录、不收集个人信息、不做付费抽卡，并公开概率。
- TikTok Mini Games 当前更像 approved partner 能力，不应作为个人开发者第一路径。

## [2026-05-03] domain | 增加海外付费小游戏路线评估

根据用户将海外方向改为收费模式的需求，新增独立海外小游戏领域，避免把海外支付、平台分成、年龄分级和合规规则混入抖音领域。

新增：

- 海外小游戏-领域总览
- 海外小游戏-付费路线评估
- 海外小游戏-资料地图
- 抖音西游抽卡小游戏-海外付费需求确认

关键结论：

- 海外付费可以绕开国内版号瓶颈，但会转向支付、税务、退款、隐私、年龄分级、平台分成和随机物品披露问题。
- 第一版建议做英文 Web / itch.io 付费验证。
- 优先采用买断或 pay-what-you-want，不建议第一版做付费抽卡。

## [2026-05-03] domain | 增加欧美市场进入框架

新增：

- 海外小游戏-欧美市场进入框架

关键框架：

```text
市场定位
  -> 小样验证
  -> 付费验证
  -> 内容获客
  -> 平台扩张
  -> 商业化加深
```

该框架把欧美小游戏进入路径拆成五层：人群、产品、商业、分发、合规。当前建议仍是先做英文 Web / itch.io 付费验证，再决定是否进入 App Store、Google Play 或 Steam。

## [2026-05-03] domain | 增加内容漏斗接小游戏模式

新增：

- 海外小游戏-内容漏斗接小游戏模式

关键结论：

- “做内容，然后在中间接小游戏”适合个人开发者做欧美市场验证。
- 该模式应按“短视频内容 -> 角色 / 世界观 / 情绪钩子 -> 可试玩小游戏 -> 付费解锁 / itch.io / 官网 -> 用户沉淀”执行。
- 小游戏早期不必在 TikTok Minis 内运行，优先作为 Web / itch.io 互动入口。
- 第一版继续避免付费随机抽卡，优先买断、PWYW 或完整版解锁。

## [2026-05-03] domain | 增加无海外银行卡变现路径

新增：

- 海外小游戏-无海外银行卡变现路径

关键结论：

- 没有国外银行卡不等于不能做海外变现，关键是平台是否支持对应收款和提现路径。
- 当前最适合个人开发者的第一路径是 itch.io Payouts + Payoneer，备选 PayPal China。
- Google Play、App Store、Steam 都更适合产品验证后进入。
- 执行前应先做小额真实购买和提现测试，记录到账时间、手续费、汇率损耗和风控问题。

## [2026-05-03] domain | 增加海外小游戏问题解决方案矩阵

新增：

- 海外小游戏-问题解决方案矩阵

用途：

- 把海外付费小游戏涉及的收款、平台、合规、产品、获客和运营问题收束成可执行矩阵。
- 当前建议的一揽子方案是 `v0.2 海外内容漏斗 + itch.io 付费验证版`。
- 推荐先做 itch.io + Payoneer 小额收款和提现测试，再投入内容流量。

## [2026-05-03] domain | 增加海外小游戏第一桶金执行手册

新增：

- 海外小游戏-第一桶金执行手册

目标：

- 30 天内完成 10-30 笔海外小额付款，累计收入 50-100 美元，并完成至少 1 次提现测试。

推荐路线：

```text
Mythic Journey 英文 Web 小游戏
  -> TikTok / YouTube Shorts / Reddit 内容导流
  -> itch.io 付费 / pay-what-you-want
  -> Payoneer 或 PayPal China 收款
  -> 提现到中国大陆银行账户
```

## [2026-05-03] domain | 增加单人优先与多人边界

新增：

- 海外小游戏-单人优先与多人边界

关键结论：

- 海外完整版付费第一版应做单人应用，不做实时多人。
- 多人会引入账号、后端、实时同步、隐私、内容审核、防作弊和服务器成本。
- 第一桶金阶段应先验证试玩、付费和提现链路，用分享图、评论投票、itch.io devlog 等低成本方式制造社区感。

## [2026-05-03] project | 启动海外解压小游戏换题确认

用户判断原抽卡游戏闭环不足，要求换一个解压小游戏方向。

新增：

- 海外解压小游戏选题框架
- 海外解压小游戏换题-需求确认

当前建议：

- 停止把抽卡作为第一桶金默认方案。
- 新方向优先考虑“整理收纳”，备选“清洁修复”和“填色 / 涂装”。
- 确认前不进入详细搜索、规划或实现。

## [2026-05-03] project | 新增数字球跑酷候选方向

用户提出新的解压小游戏候选：

```text
一颗球自动向前跑，玩家左右移动，穿过数字规则变大 / 变小，途中躲避障碍。
```

更新：

- 海外解压小游戏选题框架
- 海外解压小游戏换题-需求确认

当前判断：

- 该方向比抽卡更有即时闭环，适合 Canvas MVP 和短视频展示。
- 它更接近轻挑战跑酷，需确认是否仍按“解压”定位，还是改为“轻量休闲跑酷”。
- 暂不进入实现，先等待需求版本确认。

## [2026-05-03] project | 明确数字规则球跑酷核心规则

用户补充数字球跑酷规则：

- 障碍物有多种形状类型。
- 触碰规则包括加、减、乘、除、隐身、减速。
- 数字球碰到障碍后按规则改变当前数值或状态。
- 每一关有最小通关数值。
- 到终点时当前数值低于最小通关数值则 game over。

更新：

- 海外解压小游戏换题-需求确认
- 海外解压小游戏选题框架

当前候选名称调整为“数字规则球跑酷 / Number Rule Runner”。

## [2026-05-03] project | 确认数字规则球跑酷部分细则

用户确认：

- 当前数值大小应该影响球的视觉大小。
- 除法默认向下取整。
- 减速等状态规则正面和负面都可以存在。

更新：

- 海外解压小游戏换题-需求确认
- 海外解压小游戏选题框架

仍待确认：

- 减速负面是降低前进速度，还是降低左右移动响应。
- 失败后是否立即重试。

## [2026-05-03] project | 数字规则球跑酷 v0.1 去掉隐身

用户确认隐身先去掉，不进入 v0.1。

更新：

- 海外解压小游戏换题-需求确认
- 海外解压小游戏选题框架

当前 v0.1 状态规则只保留减速，数值规则保留加、减、乘、除。

## [2026-05-03] project | 确认 Slow- 和加法规则

用户确认：

- `Slow-` 表示负面减速，降低当前前进速度。
- 加法是 v0.1 核心数值规则之一。

更新：

- 海外解压小游戏换题-需求确认
- 海外解压小游戏选题框架

## [2026-05-03] project | 确认数字规则球跑酷路线选择要求

用户确认：

- 每个关键通道至少要有 2 条路线可供选择。

设计含义：

- 玩法从被动碰撞变成路线选择。
- 关卡应提供“安全低收益”和“高风险高收益”等可读分叉。
- 每条路线都应有通关机会，避免单一路线永远最优。

更新：

- 海外解压小游戏换题-需求确认
- 海外解压小游戏选题框架

## [2026-05-03] project | 修正数字规则球跑酷失败判定

用户修正：

- 不是到达终点才结算。
- 只要过程中当前数字低于最低数值，就立即 game over。

更新：

- 海外解压小游戏换题-需求确认
- 海外解压小游戏选题框架

当前语义从“最小通关数值”调整为“最小生存数值”。

## [2026-05-03] project | 评审数字规则球跑酷需求

新增：

- 海外解压小游戏换题-需求评审

评审结论：

- 当前玩法闭环已经清楚，但定位更接近轻挑战跑酷，不是纯解压。
- `Slow+` 和 `Slow-` 语义容易混淆，建议 v0.1 先只做加、减、乘、除，或把 `Slow-` 改成降低左右移动响应。
- 球视觉大小和碰撞半径需要分离，避免大球变成负收益。
- 第一桶金手册仍有抽卡旧表述，确认新方向后需要同步更新。

## [2026-05-03] project | 清理旧方向并补充障碍物设计

根据用户要求，清除当前主线中不再需要的旧方向内容：

- 海外解压小游戏换题-需求确认 收束为数字规则球跑酷。
- 海外小游戏-第一桶金执行手册 从抽卡示例改为 Number Rule Runner。

新增：

- 海外解压小游戏换题-障碍物设计

关键设计：

- v0.1 核心障碍为加、减、乘、除。
- `Slow-` 暂作为可选状态障碍，不建议放进前 3 关。
- 每个关键通道至少 2 条路线，路线要体现安全低收益和高风险高收益。

## [2026-05-03] project | 增加关卡专家框架和前三关草案

新增：

- 海外解压小游戏换题-关卡专家框架
- 海外解压小游戏换题-前三关设计草案

关键方法：

- 前三关采用 `teach -> test -> twist`。
- 第 1 关教加减和最低生存值。
- 第 2 关测试乘除和顺序判断。
- 第 3 关加入路障和风险路线。

资料依据：

- The Level Design Book 的 pacing、critical path、beat sheet 和 `teach -> test -> twist` 方法。
- Raph Koster 关于 fun 来自识别模式并执行行动的游戏设计观点。

## [2026-05-03] project | 增加数字规则球跑酷开发前检查清单

新增：

- 海外解压小游戏换题-开发前检查清单

用途：

- 在开发前确认需求边界、核心玩法、数值规则、关卡数据、障碍设计、手感参数、UI 信息、视觉风格、数据结构、测试标准和商业化占位。

建议默认：

- v0.1 暂时去掉 `Slow-`。
- 失败后立即重试本关。
- 视觉风格先用极简霓虹。

## [2026-05-03] project | 确认数字规则球跑酷 v0.1 开发前决策

用户确认开发前最后三项决策：

- v0.1 去掉 `Slow-`。
- 失败后立即重试本关。
- 视觉风格先用极简霓虹。

更新：

- 海外解压小游戏换题-需求确认
- 海外解压小游戏换题-开发前检查清单
- 海外解压小游戏换题-障碍物设计
- 海外解压小游戏换题-需求评审

当前 v0.1 需求版本已确认，可以进入原型开发。

## [2026-05-03] implementation | 实现 Number Rule Runner v0.1 原型

新增 Web/Canvas 原型：

- `apps/Number Rule Runner/`
- 海外解压小游戏换题-v0.1实现记录

实现：

- 3 个试玩关卡。
- 加、减、乘、除数值门。
- 除法向下取整。
- 当前数值低于最小生存值立即失败。
- 到达终点通关。
- 球视觉大小随数值变化。
- 基础路障。
- 失败立即重试。
- 极简霓虹视觉。

验证：

- `test.html` 显示 `ALL_TESTS_PASSED`。
- Chrome headless 生成移动宽度预览截图成功。
- `index.html` 静态引用检查通过。

## [2026-05-03] implementation | 继续开发 Number Rule Runner 试玩可读性

更新：

- `apps/Number Rule Runner/` 增加安全余量 HUD。
- `apps/Number Rule Runner/` 增加下一组左 / 中 / 右规则门预告。
- 路障现在在预告和画布中显示 `BLOCK`。
- Demo 完成文案改为明确提示完整版包含 30 关、赛道和球皮肤。
- 海外解压小游戏换题-v0.1实现记录

验证：

- Chrome headless 打开 `test.html`，显示 `ALL_TESTS_PASSED`。

## [2026-05-04] tooling | 增加 Number Rule Runner 无尽模式调参面板

新增：

- 海外解压小游戏换题-无尽模式调参面板

实现：

- `index.html` 增加 `Tune` 按钮和调参面板。
- 面板显示时间、距离、难度、速度、障碍间距、障碍数量和下一组路线。
- 面板提供 `1m`、`5m`、`10m`、`D5`、`D10` 跳转按钮。
- `generator.js` 增加时间 / 距离换算和障碍组状态推算。
- `game.js` 增加 `jumpToElapsed()` 和 `jumpToDifficulty()`。
- `test.html` 增加时间距离换算、调试跳转和障碍再生成测试。

验证：

- Chrome headless 打开 `test.html`，显示 `ALL_TESTS_PASSED`。
- Chrome headless 重新生成 390x844 移动预览截图成功，Tune 按钮在 HUD 下方可见。

## [2026-05-04] mechanic | 增加 Number Rule Runner Combo 机制

新增：

- 海外解压小游戏换题-combo机制

实现：

- `Game` 增加 `combo` 和 `bestCombo`。
- `+N` 和 `xN` 增加 combo。
- `-N`、`/N` 和 `BLOCK` 断 combo。
- 每 5 combo 给一次小额数值奖励和浮字反馈。
- HUD 增加 `COMBO` 状态。
- Canvas 浮字增加 combo 色彩。
- `test.html` 增加 combo 增加、断连、best combo 和 5 combo 奖励测试。

验证：

- Chrome headless 打开 `test.html`，显示 `ALL_TESTS_PASSED`。
- Chrome headless 重新生成 390x844 移动预览截图成功。

## [2026-05-04] mechanic | 增加 Number Rule Runner Fever 机制

新增：

- 海外解压小游戏换题-fever机制

实现：

- `10 combo` 触发 6 秒 Fever。
- Fever 中 `+N` 收益翻倍。
- Fever 中 `-N` 损失减半。
- Fever 中 `/N` 除数降低一档，最低 `/2`。
- Fever 中撞 `BLOCK` 仍弹开，但不断 combo。
- HUD 增加 `FEVER` 状态。
- Canvas 中 Fever 时球体发光更强，浮字增加 Fever 色。
- `test.html` 增加 Fever 触发、倒计时、收益修正和路障不断连测试。

验证：

- Chrome headless 打开 `test.html`，显示 `ALL_TESTS_PASSED`。
- Chrome headless 重新生成 390x844 移动预览截图成功。

## [2026-05-04] mechanic | 增加 Number Rule Runner Shield 机制

新增：

- 海外解压小游戏换题-shield机制

实现：

- 新增 `SHIELD` 特殊门，拾取后获得 1 层护盾，最多 1 层。
- 护盾抵消下一次 `-N`、`/N` 或 `BLOCK`，并在抵消后消耗。
- 被护盾抵消的负面效果不改变数值、不撞开玩家、不打断 combo。
- 生成器从中后段开始加入护盾路线，保留 10 分钟安全路线。
- HUD 增加 `SHIELD` 状态，Canvas 增加蓝色六边形护盾门、护盾安全环和护盾浮字。
- `test.html` 增加护盾拾取、上限、抵消、消耗、combo 保持和生成器护盾投放测试。

验证：

- Chrome headless 打开 `test.html`，显示 `ALL_TESTS_PASSED`。

## [2026-05-04] balance | 增强 Number Rule Runner 惩罚压力

用户反馈“小孩都可以跑很久”，说明当前失误代价不足。

新增：

- 海外解压小游戏换题-惩罚压力调优

实现：

- `BLOCK` 从纯弹开改为弹开并造成擦伤扣分。
- 新增 `SPIKE` 尖刺陷阱，中后段出现，按固定值和当前数值百分比取较大值扣分。
- 尖刺会打断 combo，可被 `SHIELD` 抵消。
- Fever 中路障擦伤减半，保留短暂强势体验。
- 生成器在难度 4 之后逐步加入尖刺路线，同时保留正收益安全路线。
- `test.html` 增加路障扣分、Fever 减伤、尖刺重罚、护盾抵消尖刺和尖刺生成测试。

验证：

- Chrome headless 打开 `test.html`，显示 `ALL_TESTS_PASSED`。

## [2026-05-04] balance | 放大 Number Rule Runner 路障扣分

用户反馈 `BLOCK` 擦伤数值偏小。

更新：

- `BLOCK` 擦伤扣分整体放大为 10 倍。
- Fever 中仍然按放大后的扣分减半。
- 护盾仍然可以完全抵消 `BLOCK`。
- `test.html` 同步更新普通路障和 Fever 路障扣分断言。
- 海外解压小游戏换题-惩罚压力调优 同步记录 10 倍擦伤规则。

验证：

- Chrome headless 打开 `test.html`，显示 `ALL_TESTS_PASSED`。

## [2026-05-04] mechanic | 增加 Number Rule Runner Grip 机制

用户反馈只要左右滑动就很容易跑很久，需要削弱横滑反应的万能性。

新增：

- 海外解压小游戏换题-grip机制

实现：

- 新增 `GRIP` 抓地力资源，初始 100。
- 横向快速移动会消耗抓地力，稳定操作会恢复抓地力。
- 抓地力低时横移响应变慢。
- 抓地力耗尽后继续猛滑会触发 `SKID -N` 打滑扣分，并在非 Fever 状态下打断 combo。
- Fever 中打滑扣分减半。
- HUD 增加 `GRIP` 状态，低抓地时高亮警示。
- Canvas 在低抓地时用橙色安全环提示操作不稳定。
- `test.html` 增加抓地力消耗、耗尽、打滑扣分、低抓地转向变慢、稳定恢复和快照输出测试。

验证：

- Chrome headless 打开 `test.html`，显示 `ALL_TESTS_PASSED`。

## [2026-05-04] mechanic | 改造 Number Rule Runner Grip 为触发式

用户反馈 `GRIP` 抓地力机制只应在特定时间段触发，例如吃到抓地力障碍后。

更新：

- 平时显示 `GRIP OFF`，横向移动不消耗抓地力。
- 新增 `SLIP` 障碍，命中后开启限时抓地力挑战。
- 抓地力挑战期间才会消耗 `GRIP`、低抓地转向变慢、耗尽后触发 `SKID -N`。
- `SHIELD` 可以抵消 `SLIP`，不进入抓地力挑战。
- 生成器从中段开始投放 `SLIP`。
- HUD、Canvas、测试和 海外解压小游戏换题-grip机制 同步改为触发式规则。

验证：

- Chrome headless 打开 `test.html`，显示 `ALL_TESTS_PASSED`。

## [2026-05-04] balance | 增加 Number Rule Runner 数值阶段曲线

用户反馈加减法数值不应该固定，后期应该越来越大。

新增：

- 海外解压小游戏换题-数值阶段曲线

实现：

- `EndlessGenerator` 增加 `valueStageAt()` 和 `stagedValuesAt()`。
- 每 3 个难度推进一个数值阶段。
- 小加法、大加法和减法都按阶段增长，并保留上限防止数值失控。
- `window.NRR.math` 暴露阶段曲线函数，方便测试和调参。
- `README.md` 增加加减法按阶段增长说明。
- `test.html` 增加阶段推进、加法增长、减法增长和实际生成值增长测试。

验证：

- Chrome headless 打开 `test.html`，显示 `ALL_TESTS_PASSED`。

## [2026-05-04] mechanic | 增加 Number Rule Runner Target Zone 机制

根据算法定制创新玩法：目标区间门让玩家主动控制当前数值，而不是无脑堆高。

新增：

- 海外解压小游戏换题-target-zone机制

实现：

- 新增 `target` 障碍类型，显示为 `min-max`。
- 当前数值在区间内时获得小额奖励并增加 combo。
- 当前数值低于区间时按低于幅度加重扣分并断 combo。
- 当前数值高于区间时按溢出幅度加重扣分并断 combo。
- `SHIELD` 不抵消 Target 失败，Fever 不放大 Target 奖励。
- `EndlessGenerator` 增加 `targetZoneAt()`，Target 区间随阶段上移并变窄。
- 生成器从难度 3 后开始投放 Target。
- Canvas、路线预告、README 和测试同步支持 Target。

验证：

- Chrome headless 打开 `test.html`，显示 `ALL_TESTS_PASSED`。

## [2026-05-04] balance | 调整 Number Rule Runner 首分钟难度

用户反馈当前难度仍偏简单，玩家容易玩一分钟就放弃。

新增：

- 海外解压小游戏换题-首分钟难度调优

实现：

- 难度距离从 `12000` 缩短到 `9000`，更快进入 D2/D3。
- 起始速度从 `225` 提升到 `235`，最高速度从 `315` 提升到 `335`。
- 路组间距从 `330-250` 收紧到 `305-225`，第一分钟决策密度更高。
- `TARGET` 和 `SLIP` 从 D2 开始出现。
- `SPIKE` 从 D3 开始进入部分路线。
- `jumpToDifficulty()` 改为读取生成器 `difficultyDistance`，调试跳转与曲线保持一致。
- `test.html` 增加首分钟进入压力难度、首分钟生成 Target 和 SLIP 的测试。

验证：

- Chrome headless 打开 `test.html`，显示 `ALL_TESTS_PASSED`。

## [2026-05-04] sound | 增加 Number Rule Runner 音效系统

用户反馈当前没有音效，需要重新开始设计音频反馈。

新增：

- 海外解压小游戏换题-音效系统设计
- `apps/Number Rule Runner/js/audio/sound.js`

实现：

- 使用 Web Audio API 程序化生成音效，不依赖外部音频文件。
- `Game` 增加声音事件队列 `queueSound()` 和 `drainSoundEvents()`。
- `app.js` 每帧消费声音事件并交给 `SoundEngine` 播放。
- 首次点击、按键或 Start/Restart 时解锁浏览器音频。
- 覆盖正收益、负收益、Target、Combo、Fever、Shield、Block、Spike、Slip、Skid、Game Over 等声音事件。
- `test.html` 增加 SoundEngine 可用、核心事件排队音效和队列一次性消费测试。

验证：

- Chrome headless 打开 `test.html`，显示 `ALL_TESTS_PASSED`。
- Chrome headless 重新生成 390x844 移动预览截图成功。

## [2026-05-04] sound | 增加 Number Rule Runner 轻松背景音乐

用户要求设计轻松欢快的背景音乐。

实现：

- 在 `SoundEngine` 中增加程序化背景音乐循环，不依赖外部音频文件。
- 背景音乐使用 116 BPM、C 大调五声音阶旋律、轻量低音脉冲和柔和和弦铺底。
- 音频解锁后自动启动背景音乐。
- 背景音乐音量低于规则反馈音，避免遮盖加减、Target、Spike、Fever 等关键反馈。
- `SoundEngine` 增加 `startMusic()`、`stopMusic()`、`scheduleMusic()` 等调度方法。
- `test.html` 增加背景音乐控制方法可用性测试。
- 海外解压小游戏换题-音效系统设计 同步记录背景音乐设计。

验证：

- Chrome headless 打开 `test.html`，显示 `ALL_TESTS_PASSED`。

## [2026-05-04] balance | 改造 Number Rule Runner 为多排窗口难度

用户要求提高难度：速度、横排不一定有最优解、不要每一排都保证有 `+` 或 `x`。

新增：

- 海外解压小游戏换题-多排窗口难度

实现：

- 生成器 `phase 3` 在 D2 后改为 `/2 or /3`、`SLIP`、`TARGET`，无 `+` 或 `x` 快捷门。
- 生成器 `phase 7` 在 D3 后改为 `SPIKE`、`/2`、`TARGET`，无 `+` 或 `x` 快捷门。
- `test.html` 的 10 分钟模拟改为智能选择每排最好结果，而不是只找 `+` / `x`。
- `test.html` 增加后期存在无 `+` / `x` 横排的验证。
- `test.html` 增加每 4 排窗口内仍存在恢复或控值机会的验证。
- `README.md` 增加多排窗口难度说明。

验证：

- Chrome headless 打开 `test.html`，显示 `ALL_TESTS_PASSED`。

## [2026-05-04] balance | 大幅增加 Number Rule Runner 抓地力障碍

用户要求抓力器出现次数大幅增加。

更新：

- `SLIP` 在 `phase 1` 从 D2 开始替换中路减法。
- `SLIP` 在 `phase 6` 从 D2 开始替换中路护盾/减法位置。
- 保留原有 `phase 3` 和 `phase 5` 的 `SLIP`。
- 中期生成测试要求至少出现 3 个 `SLIP`。
- 后期生成测试要求至少出现 4 个 `SLIP`，且 8 排中至少一半包含湿滑压力。
- README 和 海外解压小游戏换题-grip机制 同步记录高频 `SLIP` 规则。

验证：

- Chrome headless 打开 `test.html`，显示 `ALL_TESTS_PASSED`。

## [2026-05-04] balance | 修复 Number Rule Runner 无尽模式挂机风险

再次测试发现：

- `999` 数值上限让乘法后的容错过厚，后续风险容易失效。
- 中路模板长期偏安全时，玩家可能站中路挂机跑很久，削弱主动路线选择。

修复：

- `endlessConfig.maxValue` 从 `999` 下调到 `199`。
- `EndlessGenerator` 调整中路模板，让中路周期性出现减法、除法或路障。
- 左右两侧仍保留主动安全选择，避免破坏 10 分钟可玩目标。
- `test.html` 增加“站中路不是 10 分钟策略”的测试。
- 更新 海外解压小游戏换题-无尽模式设计 和 海外解压小游戏换题-无尽模式评判专家评审。

验证：

- Chrome headless 打开 `test.html`，显示 `ALL_TESTS_PASSED`。

## [2026-05-04] fix | 修复 Number Rule Runner 无尽模式长跑问题

发现问题：

- 连续乘法会让当前数值指数膨胀，长跑后 HUD 和球面文字不可读，极端情况下可能出现无限大。
- 10 分钟测试只验证了安全路线存在，未验证数值是否保持有界。
- 开始页背后渲染了赛道障碍，视觉噪音偏多。
- 进度条短周期循环，不符合“难度缓慢递增”的反馈。

修复：

- `endlessConfig` 增加 `maxValue: 999`。
- `Game.applyObstacle()` 对加、减、乘、除结果做数值边界处理。
- `snapshot()` 输出 `displayValue`，HUD 和球面使用可读显示值。
- `test.html` 增加乘法封顶、10 分钟数值有界和长周期难度进度测试。
- `Renderer` 在 ready 状态隐藏赛道障碍，让开始页更干净。
- 进度条改为当前难度段的长周期进度。
- 更新 海外解压小游戏换题-无尽模式设计 和 海外解压小游戏换题-v0.3无尽模式实现记录。

验证：

- Chrome headless 打开 `test.html`，显示 `ALL_TESTS_PASSED`。
- Chrome headless 重新生成 390x844 移动预览截图成功。

## [2026-05-04] refactor | 评判专家修复 Number Rule Runner 无尽模式

新增：

- 海外解压小游戏换题-无尽模式评判专家评审
- `apps/Number Rule Runner/js/core/generator.js`
- `apps/Number Rule Runner/js/core/storage.js`

专家评审问题与修复：

- 系统架构专家：`Game` 同时承担状态、碰撞和难度生成，已拆出 `EndlessGenerator`。
- 留存与回玩专家：无尽模式未保存最佳时间，已用 `localStorage` 保存 best time，存储不可用时静默降级。
- 移动端输入专家：只处理 `pointerup`，已补 `pointercancel` 和 `lostpointercapture`。
- 测试专家：测试现在直接验证生成器、长跑安全路线、数值边界和有效障碍类型。

验证：

- Chrome headless 打开 `test.html`，显示 `ALL_TESTS_PASSED`。
- Chrome headless 重新生成 390x844 移动预览截图成功。

## [2026-05-03] implementation | 改造 Number Rule Runner 为无尽模式

用户反馈固定通关会打断，需要至少能跑 10 分钟、难度缓慢递增的无尽模式。

新增：

- 海外解压小游戏换题-无尽模式设计
- 海外解压小游戏换题-v0.3无尽模式实现记录

更新：

- `apps/Number Rule Runner/js/data/levels.js` 从固定关卡数组改为 `endlessConfig`。
- `apps/Number Rule Runner/js/core/game.js` 改为动态生成障碍组，移除 finish / clear / complete 结算。
- `apps/Number Rule Runner/js/app.js` 和 `index.html` 将 HUD 第一项改为时间，Game Over 显示本局时间和最佳时间。
- `apps/Number Rule Runner/test.html` 增加 10 分钟配置级可玩性验证。
- `app.manifest.json` 更新为 `v0.3-prototype`。

设计结论：

- 最低生存值保持稳定，不随时间自动上涨，避免无碰撞也突然死亡。
- 难度通过速度、障碍间距、路障频率和负面门强度缓慢递增。
- 10 分钟距离内每组障碍都保留非打断选择。

验证：

- Chrome headless 打开 `test.html`，显示 `ALL_TESTS_PASSED`。

## [2026-05-03] implementation | 扩展 Number Rule Runner 到 10 关

根据关卡专家框架先完成十关设计，再开发关卡数据。

新增：

- 海外解压小游戏换题-十关设计草案
- 海外解压小游戏换题-v0.2十关实现记录

更新：

- `apps/Number Rule Runner/js/data/levels.js` 从 3 关扩展到 10 关。
- `apps/Number Rule Runner/test.html` 增加十关数量、路线选择组、配置级可通路线测试。
- `apps/Number Rule Runner/app.manifest.json` 更新为 `v0.2-prototype`。
- `apps/Number Rule Runner/README.md` 更新为 10 关试玩范围。
- `wiki/index.md` 增加 v0.2 设计和实现记录入口。

验证：

- Chrome headless 打开 `test.html`，显示 `ALL_TESTS_PASSED`。
- Chrome headless 重新生成 390x844 移动预览截图成功。


## [2026-05-06] maintenance

Validated wiki-service parsing, healthcheck, HTTP filters, and log endpoint after continuing Easy Wiki construction.


## [2026-05-06] structure

Narrowed the main easy-wiki repo to the core wiki/access-layer path. Moved apps to C:/Code/easy-wiki-apps and moved non-core domain expansion assets to C:/Code/easy-wiki-domain-expansion. Updated indexes, scope docs, and health checks accordingly.

## [2026-05-06] implementation

Implemented a basic MCP stdio server for easy-wiki with initialize, tools/list, and tools/call support backed by wiki_core.py. Verified wiki_read_page and wiki_healthcheck through a local MCP session.

## [2026-05-06] implementation

Added batch raw scanning and compile support. New script scan_raw.py, HTTP endpoints /compile-missing-sources and /scan-raw, and MCP tool wiki_compile_missing_sources now detect raw files without source pages and can compile them in batch.

## [2026-05-06] ingest

Added 10 new raw film/television expert originals for batch compile testing: 5 DGA director interviews and 5 American Cinematographer articles. These raw files are intentionally left uncompiled so scan_raw and compile_missing_sources can detect them.

## [2026-05-06] implementation

Improved raw batch compile quality in `wiki-service`: dry-run batch scans now report `would_write_count` and `would_write_source_ids` instead of treating preview items as skipped, and raw source compilation now separates top-of-file source metadata from article body so summaries, claims, keywords, and generated draft metadata are cleaner.

## [2026-05-06] docs

Refactored the architecture documentation to reflect the current scoped-down Easy Wiki reality. Rewrote `docs/overall-architecture.md`, `docs/core-knowledge-architecture.md`, and `docs/function-boundaries.md` around the actual implemented HTTP and MCP access layer, clarified the architecture route, and documented the main strengths, weaknesses, and next improvements.

## [2026-05-06] implementation

Strengthened the core wiki-service loop in three high-value ways: compiled source drafts now carry lifecycle tracking (`review_status`, `promotion_status`, `compiled_at`, `compile_version`), `healthcheck` now reports pending-review drafts and drafts missing tracking fields, and a first automated unittest suite now covers raw parsing, compile draft generation, batch dry-run semantics, and draft tracking behavior.

## [2026-05-06] ingest

Added 10 new cross-border ecommerce raw originals for compile testing:

- `raw/juozas-kaziukenas-amazon-crackdown-raw.md`
- `raw/aaron-rubin-omnichannel-ecommerce-raw.md`
- `raw/james-thomson-brand-control-raw.md`
- `raw/greg-mercer-jungle-stix-lessons-raw.md`
- `raw/kiri-masters-ad-channel-right-brand-raw.md`
- `raw/michael-michelini-cross-border-lessons-raw.md`
- `raw/kevin-king-top-10-secret-amazon-hacks-raw.md`
- `raw/alex-yancher-smarter-paths-global-sales-raw.md`
- `raw/oksana-tsvigun-us-market-testing-raw.md`
- `raw/bradley-sutton-dropshipping-case-study-raw.md`

Validated that `scan_raw.py` detects the new files and that compile dry-run works on the new Alex Yancher source.

## [2026-05-07] implementation

Added the first minimal execution governance layer under `services/governance/`. The new layer defines generic artifacts, step contracts, governance decisions, input resolution strategies, and trace records so external apps can use wiki knowledge with explicit input and provenance rules. Added governance docs, core policy examples, and unit tests.

## [2026-05-07] docs

Added a root `README.md` that explains Easy Wiki's role as the core wiki platform, documents the repository layout, links key architecture/service/governance docs, and clarifies the boundary with `easy-wiki-studio`.

## [2026-05-07] docs

Added `README.zh-CN.md` and language switch links between the English and Chinese root README files.
