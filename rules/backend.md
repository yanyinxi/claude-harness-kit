# Backend Rules Templates

> ⚠️ **注意**: 这些是后端开发规则模板，实际规则应根据具体项目技术栈创建。

## 技术栈检测

这些规则模板通过路径自动匹配项目类型：

| 技术栈 | 检测路径 |
|--------|---------|
| Java/Spring | `**/*.java` |
| Python/Django | `**/*.py` |
| Node/Express | `**/*.js`, `**/*.ts` |
| Go | `**/*.go` |
| Rust | `**/*.rs` |

## 通用后端最佳实践

### 1. 异常处理

统一异常处理，避免泄露内部细节：

```java
// ✅ 正确：统一异常类型
throw new ApiException(404, "Resource not found");
throw new ApiException(400, "Invalid parameter: " + field);
```

```java
// ❌ 错误：直接抛出原始异常
throw new RuntimeException("Database error");
```

### 2. SQL注入防护

使用参数化查询，禁止字符串拼接：

```java
// ✅ 正确：参数化查询
List<User> users = userMapper.selectByMap(params);

// ❌ 错误：字符串拼接
String sql = "SELECT * FROM users WHERE id = " + userId;
```

### 3. 输入验证

所有外部输入必须验证：

```java
// ✅ 正确：验证输入
if (id == null || id <= 0) {
    throw new ApiException(400, "Invalid id");
}
```

### 4. 日志规范

不记录敏感信息：

```java
// ✅ 正确：脱敏日志
logger.info("User login: {}", maskEmail(email));

// ❌ 错误：记录敏感信息
logger.info("Password: {}", password);
```

### 5. 并发安全

使用线程安全的数据结构：

```java
// ✅ 正确：线程安全
private final ConcurrentHashMap<String, Cache> cache =
    new ConcurrentHashMap<>();

// ❌ 错误：非线程安全
private final HashMap<String, Cache> cache = new HashMap<>();
```

## 数据库最佳实践

### ORM使用原则

| 操作 | 建议 |
|------|------|
| 简单CRUD | 使用框架提供的Mapper/Repository |
| 复杂查询 | 使用XML/Query DSL |
| 批量操作 | 批次处理，避免OOM |

### 事务管理

```java
// ✅ 正确：明确事务边界
@Transactional(rollbackFor = Exception.class)
public void updateBatch(List<Entity> entities) {
    // 事务操作
}
```

## API设计原则

### RESTful规范

| 方法 | 用途 | 示例 |
|------|------|------|
| GET | 查询 | `GET /users` |
| POST | 创建 | `POST /users` |
| PUT | 更新 | `PUT /users/{id}` |
| DELETE | 删除 | `DELETE /users/{id}` |

### 统一响应格式

```json
{
  "code": 200,
  "message": "success",
  "data": {}
}
```

## 安全最佳实践

### 认证授权

```java
// ✅ 正确：使用框架安全机制
@PreAuthorize("hasRole('ADMIN')")
public void deleteUser(Long id) {
    // 仅管理员可执行
}
```

### 数据脱敏

```java
// 手机号脱敏：138****5678
public String maskPhone(String phone) {
    if (phone == null || phone.length() < 11) return phone;
    return phone.substring(0, 3) + "****" + phone.substring(7);
}
```

---

## 📈 合规统计

此文件为模板，合规统计应在实际项目中追踪。

_最后更新: 2026-04-30_
