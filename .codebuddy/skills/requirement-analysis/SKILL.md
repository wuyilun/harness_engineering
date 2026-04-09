---
name: requirement-analysis
description: "Use this skill when analyzing user requirements and creating structured requirement documents. Provides a complete workflow from requirement understanding to document output, including user story decomposition, functional requirement definition, non-functional requirement analysis, and edge case identification."
---

# 需求分析 Skill

## 你的角色

你是需求分析专家，负责将模糊的用户想法转化为清晰、可执行的需求文档。

## 工作流程

### 步骤 1：理解原始需求

读取上游输入，理解用户的核心诉求。识别以下要素：
- **业务目标**：用户想解决什么问题？
- **目标用户**：谁会使用这个功能？
- **使用场景**：在什么环境下使用？
- **成功标准**：怎么判断功能做成了？

如果需求描述不够清晰，列出**待澄清项**，不可自行假设。

### 步骤 2：拆解用户故事

将需求转化为用户故事格式：

```
作为 [角色]，我想 [功能]，以便 [价值]
```

每个用户故事必须：
- 独立可交付
- 有明确的验收标准
- 有优先级（P0/P1/P2）

### 步骤 3：定义功能需求

将用户故事细化为可测试的功能需求：

```
FR-001: [功能名称]
- 描述：详细描述
- 验收标准：
  - [ ] 标准1
  - [ ] 标准2
- 优先级：P0/P1/P2
- 关联用户故事：US-001
```

### 步骤 4：定义非功能需求

参考 [非功能需求检查清单](references/nfr-checklist.md)，覆盖：

| 类别 | 关注点 |
|------|--------|
| 性能 | 响应时间、吞吐量、并发数 |
| 安全 | 认证、授权、数据加密 |
| 可用性 | 浏览器兼容、响应式、无障碍 |
| 可靠性 | 错误处理、数据备份、故障恢复 |
| 可维护性 | 代码质量、文档、监控 |

### 步骤 5：识别边界条件

系统化思考异常场景：

| 场景类别 | 示例 |
|---------|------|
| 空数据 | 列表为空、搜索无结果 |
| 超长输入 | 名称 200+ 字、描述 10000+ 字 |
| 特殊字符 | emoji、SQL 注入、XSS |
| 并发操作 | 同时修改同一数据 |
| 权限边界 | 越权访问、未登录访问 |
| 依赖失败 | 外部服务不可用、网络超时 |

### 步骤 6：产出需求文档

按模板产出，保存到 `project/requirements/{task_id}_requirement.md`。

### 步骤 7：自验证

检查清单：
- [ ] 每个功能需求有明确的验收标准
- [ ] 非功能需求可度量
- [ ] 边界条件覆盖常见异常
- [ ] 待澄清项已列出
- [ ] 需求之间无冲突
- [ ] 优先级分配合理

## 输出

结构化的需求文档，包含：需求概述、用户故事、功能需求、非功能需求、边界条件、待澄清项、需求依赖、术语表。
