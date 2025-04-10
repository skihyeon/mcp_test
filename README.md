# MCP Setup Tool

MCP(Model Control Protocol) 자동 설정 도구입니다. 커서(Cursor)에서 작동하는 다양한 MCP 서버를 손쉽게 설정할 수 있습니다.

## 기능

- MCP 서버 자동 설정
- GitHub MCP 서버 설정
- 사용자 정의 MCP 서버 추가/제거
- MCP 설정 백업 및 복원
- MCP 설정 내보내기/가져오기
- **자동 OS 감지 및 OS별 최적화 설정**
- **Node.js 설치 자동 확인**
- **MCP 패키지 자동 설치**

## 요구사항

- Python 3.6 이상
- **Node.js** (자동으로 설치 여부 확인)

## 지원 운영체제

- Windows
- macOS
- Linux

## 사용 방법

### MCP 설치 및 설정 한번에 진행 (권장)

```bash
# GitHub을 포함한 모든 MCP 설치 및 설정
python mcp_setup.py all --github-token YOUR_GITHUB_TOKEN

# GitHub 제외하고 기본 MCP 설치 및 설정
python mcp_setup.py all
```

### MCP 패키지만 설치

```bash
# GitHub을 포함한 모든 MCP 설치
python mcp_setup.py install --github-token YOUR_GITHUB_TOKEN

# GitHub 제외하고 기본 MCP 설치
python mcp_setup.py install
```

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

## 설치되는 MCP 패키지

- **Sequential Thinking MCP**
  ```
  npx -y @smithery/cli@latest install @smithery-ai/server-sequential-thinking --client cursor --key f120217f-d8f9-4b5e-b9c9-cf9feb0aad83
  ```

- **Think MCP Server**
  ```
  npx -y @smithery/cli@latest install @PhillipRt/think-mcp-server --client cursor --key f120217f-d8f9-4b5e-b9c9-cf9feb0aad83
  ```

- **GitHub MCP** (토큰 제공 시)
  ```
  npx -y @smithery/cli@latest install @smithery-ai/github --client cursor --config '{"githubPersonalAccessToken":"YOUR_GITHUB_TOKEN"}'
  ```

## 예제

### 모든 MCP 설치 및 설정 (권장)

```bash
# 설치와 설정을 한번에 진행
python mcp_setup.py all --github-token ghp_YOUR_TOKEN_HERE
```

### 개별 설치 및 설정

```bash
# 1. MCP 패키지 설치
python mcp_setup.py install --github-token ghp_YOUR_TOKEN_HERE

# 2. 기본 MCP 서버 설정
python mcp_setup.py setup

# 3. GitHub MCP 설정 (토큰 필요)
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
- **Node.js 설치 여부 자동 확인**
- **실행 전 의존성 검사**

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

- Node.js가 설치되어 있지 않으면 "Node.js가 설치되어 있어야 합니다." 메시지가 표시됩니다.
- 설정은 운영체제에 따라 다음 경로에 저장됩니다:
  - Windows: `%USERPROFILE%\.cursor\mcp.json`
  - macOS: `~/Library/Application Support/Cursor/mcp.json`
  - Linux: `~/.cursor/mcp.json`
- 백업 파일은 `./mcp_setup/backups/` 디렉토리에 저장됩니다. 