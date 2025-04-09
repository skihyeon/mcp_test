# MCP Setup Tool

MCP(Model Control Protocol) 자동 설정 도구입니다. 커서(Cursor)에서 작동하는 다양한 MCP 서버를 손쉽게 설정할 수 있습니다.

## 기능

- MCP 서버 자동 설정
- GitHub MCP 서버 설정
- 사용자 정의 MCP 서버 추가/제거
- MCP 설정 백업 및 복원
- MCP 설정 내보내기/가져오기
- **자동 OS 감지 및 OS별 최적화 설정**

## 지원 운영체제

- Windows
- macOS
- Linux

## 사용 방법

### 기본 MCP 서버 설정

```bash
python mcp_setup.py setup
```

이 명령은 다음 MCP 서버를 설정합니다:
- `think-mcp-server`
- `server-sequential-thinking`

### GitHub MCP 서버 설정

```bash
python mcp_setup.py github --token YOUR_GITHUB_TOKEN
```

### MCP 서버 추가

```bash
python mcp_setup.py add --name 서버이름 --command 명령어 --args 인자1,인자2,인자3
```

### MCP 서버 제거

```bash
python mcp_setup.py remove --name 서버이름
```

### MCP 설정 내보내기

```bash
python mcp_setup.py export --output 파일경로
```

### MCP 설정 가져오기

```bash
python mcp_setup.py import --input 파일경로
```

### MCP 설정 백업

```bash
python mcp_setup.py backup
```

### MCP 서버 목록 조회

```bash
python mcp_setup.py list
```

### 시스템 정보 확인

```bash
python mcp_setup.py sysinfo
```

## 예제

### 모든 기본 MCP 설정 (think, sequential-thinking, github)

```bash
# 기본 MCP 서버 설정
python mcp_setup.py setup

# GitHub MCP 설정 (토큰 필요)
python mcp_setup.py github --token ghp_YOUR_TOKEN_HERE
```

### 사용자 정의 MCP 서버 추가

```bash
python mcp_setup.py add --name "custom-mcp" --command "npx" --args "-y,@smithery/cli@latest,run,@smithery-ai/custom-tool,--key,키값"
```

## 특징

- 운영체제 자동 감지: Windows, macOS, Linux 환경에 맞게 자동 설정
- **Windows에서는 `cmd /c npx` 형식 사용** (업데이트됨)
- 각 OS별 Cursor 설정 경로 자동 감지
- 설정 가져오기/내보내기 시 OS 호환성 자동 처리

## OS별 명령어 형식

- **Windows**:
  ```json
  {
    "command": "cmd",
    "args": ["/c", "npx", "-y", "@smithery/cli@latest", "..."]
  }
  ```

- **macOS/Linux**:
  ```json
  {
    "command": "npx",
    "args": ["-y", "@smithery/cli@latest", "..."]
  }
  ```

## 참고사항

- 설정은 운영체제에 따라 다음 경로에 저장됩니다:
  - Windows: `%USERPROFILE%\.cursor\mcp.json`
  - macOS: `~/Library/Application Support/Cursor/mcp.json`
  - Linux: `~/.cursor/mcp.json`
- 백업 파일은 `./mcp_setup/backups/` 디렉토리에 저장됩니다. 