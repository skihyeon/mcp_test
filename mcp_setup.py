#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
import sys
import json
import shutil
import platform
import argparse
import subprocess
from pathlib import Path
from typing import Dict, List, Any, Optional

# 색상 코드
class Colors:
    HEADER = '\033[95m'
    BLUE = '\033[94m'
    CYAN = '\033[96m'
    GREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'

def print_colored(text: str, color: str):
    """컬러 텍스트 출력"""
    print(f"{color}{text}{Colors.ENDC}")

class OSInfo:
    """운영 체제 정보"""
    @staticmethod
    def get_os_type():
        """운영 체제 타입 반환"""
        system = platform.system().lower()
        if system == "darwin":
            return "macos"
        elif system == "windows":
            return "windows"
        elif system == "linux":
            return "linux"
        else:
            return "unknown"
    
    @staticmethod
    def is_windows():
        """Windows 확인"""
        return platform.system().lower() == "windows"
    
    @staticmethod
    def is_macos():
        """macOS 확인"""
        return platform.system().lower() == "darwin"
    
    @staticmethod
    def is_linux():
        """Linux 확인"""
        return platform.system().lower() == "linux"
    
    @staticmethod
    def get_home_dir():
        """홈 디렉토리 반환"""
        return Path.home()
    
    @staticmethod
    def get_os_details():
        """OS 상세 정보 반환"""
        return {
            "system": platform.system(),
            "release": platform.release(),
            "version": platform.version(),
            "machine": platform.machine(),
            "processor": platform.processor(),
            "python_version": platform.python_version()
        }

class NodeJSChecker:
    """Node.js 확인 클래스"""
    @staticmethod
    def is_nodejs_installed():
        """Node.js 설치 여부 확인"""
        try:
            # Windows와 다른 OS에 따라 명령어 조정
            cmd = "node --version" if not OSInfo.is_windows() else "cmd /c node --version"
            result = subprocess.run(cmd, shell=True, capture_output=True, text=True)
            return result.returncode == 0 and result.stdout.strip().startswith("v")
        except Exception:
            return False
    
    @staticmethod
    def get_nodejs_version():
        """Node.js 버전 반환"""
        if not NodeJSChecker.is_nodejs_installed():
            return None
        
        try:
            cmd = "node --version" if not OSInfo.is_windows() else "cmd /c node --version"
            result = subprocess.run(cmd, shell=True, capture_output=True, text=True)
            if result.returncode == 0:
                return result.stdout.strip()
            return None
        except Exception:
            return None

class MCPInstaller:
    """MCP 설치 클래스"""
    def __init__(self):
        self.os_type = OSInfo.get_os_type()
    
    def run_install_command(self, command):
        """설치 명령어 실행"""
        try:
            print_colored(f"명령 실행: {command}", Colors.CYAN)
            result = subprocess.run(command, shell=True, capture_output=True, text=True)
            
            if result.returncode == 0:
                print_colored("설치 성공!", Colors.GREEN)
                return True, result.stdout
            else:
                print_colored(f"설치 실패: {result.stderr}", Colors.FAIL)
                return False, result.stderr
        except Exception as e:
            print_colored(f"설치 명령 실행 중 오류: {str(e)}", Colors.FAIL)
            return False, str(e)
    
    def install_sequential_thinking(self):
        """Sequential Thinking MCP 설치"""
        base_cmd = "npx -y @smithery/cli@latest install @smithery-ai/server-sequential-thinking --client cursor --key f120217f-d8f9-4b5e-b9c9-cf9feb0aad83"
        
        if OSInfo.is_windows():
            cmd = f"cmd /c {base_cmd}"
        else:
            cmd = base_cmd
        
        return self.run_install_command(cmd)
    
    def install_think_server(self):
        """Think MCP Server 설치"""
        base_cmd = "npx -y @smithery/cli@latest install @PhillipRt/think-mcp-server --client cursor --key f120217f-d8f9-4b5e-b9c9-cf9feb0aad83"
        
        if OSInfo.is_windows():
            cmd = f"cmd /c {base_cmd}"
        else:
            cmd = base_cmd
        
        return self.run_install_command(cmd)
    
    def install_github(self, token):
        """GitHub MCP 설치"""
        # 토큰에서 따옴표 처리
        token = token.replace('"', '\\"')
        
        base_cmd = f'npx -y @smithery/cli@latest install @smithery-ai/github --client cursor --config "\\"{{\\\"githubPersonalAccessToken\\\":\\\"{token}\\\"}}\\"" '
        
        if OSInfo.is_windows():
            cmd = f"cmd /c {base_cmd}"
        else:
            cmd = base_cmd
        
        return self.run_install_command(cmd)
    
    def install_all_mcps(self, github_token=None):
        """모든 MCP 설치"""
        # Node.js 설치 확인
        if not NodeJSChecker.is_nodejs_installed():
            print_colored("Node.js가 설치되어 있어야 합니다.", Colors.FAIL)
            return False
        
        node_version = NodeJSChecker.get_nodejs_version()
        print_colored(f"감지된 Node.js 버전: {node_version}", Colors.CYAN)
        
        # Sequential Thinking MCP 설치
        print_colored("\n===== Sequential Thinking MCP 설치 =====", Colors.HEADER)
        success_seq, _ = self.install_sequential_thinking()
        
        # Think Server MCP 설치
        print_colored("\n===== Think Server MCP 설치 =====", Colors.HEADER)
        success_think, _ = self.install_think_server()
        
        # GitHub MCP 설치 (토큰이 제공된 경우)
        success_github = True
        if github_token:
            print_colored("\n===== GitHub MCP 설치 =====", Colors.HEADER)
            success_github, _ = self.install_github(github_token)
        
        return success_seq and success_think and success_github

class MCPSetup:
    def __init__(self):
        self.os_type = OSInfo.get_os_type()
        self.home_dir = OSInfo.get_home_dir()
        
        # OS별 Cursor 설정 경로
        if OSInfo.is_windows():
            # Windows에서는 %USERPROFILE%\.cursor
            self.cursor_dir = self.home_dir / '.cursor'
        elif OSInfo.is_macos():
            # macOS에서는 ~/Library/Application Support/Cursor
            self.cursor_dir = self.home_dir / 'Library' / 'Application Support' / 'Cursor'
        else:
            # Linux에서는 ~/.cursor
            self.cursor_dir = self.home_dir / '.cursor'
            
        self.mcp_json_path = self.cursor_dir / 'mcp.json'
        self.current_dir = Path.cwd()
        self.target_dir = self.current_dir / 'mcp_setup'
        self.backup_dir = self.target_dir / 'backups'
        
        # 필요한 디렉토리 생성
        self.backup_dir.mkdir(exist_ok=True, parents=True)
        
        # OS 정보 출력
        print_colored(f"감지된 운영 체제: {self.os_type}", Colors.CYAN)
        print_colored(f"Cursor 설정 경로: {self.cursor_dir}", Colors.CYAN)
    
    def load_mcp_config(self) -> Dict:
        """MCP 설정 파일 로드"""
        if not self.mcp_json_path.exists():
            print_colored(f"MCP 설정 파일을 찾을 수 없습니다: {self.mcp_json_path}", Colors.WARNING)
            return {}

        try:
            with open(self.mcp_json_path, 'r', encoding='utf-8') as f:
                return json.load(f)
        except json.JSONDecodeError:
            print_colored(f"MCP 설정 파일 파싱 오류: {self.mcp_json_path}", Colors.FAIL)
            return {}
        except Exception as e:
            print_colored(f"MCP 설정 파일 읽기 오류: {str(e)}", Colors.FAIL)
            return {}
    
    def backup_mcp_config(self) -> bool:
        """MCP 설정 파일 백업"""
        if not self.mcp_json_path.exists():
            print_colored("백업할 MCP 설정 파일이 없습니다.", Colors.WARNING)
            return False
        
        backup_file = self.backup_dir / f"mcp_backup_{os.urandom(4).hex()}.json"
        try:
            shutil.copy2(self.mcp_json_path, backup_file)
            print_colored(f"MCP 설정 백업 완료: {backup_file}", Colors.GREEN)
            return True
        except Exception as e:
            print_colored(f"MCP 설정 백업 오류: {str(e)}", Colors.FAIL)
            return False
    
    def save_mcp_config(self, config: Dict) -> bool:
        """MCP 설정 파일 저장"""
        try:
            # 디렉토리가 없으면 생성
            self.cursor_dir.mkdir(exist_ok=True, parents=True)
            
            with open(self.mcp_json_path, 'w', encoding='utf-8') as f:
                json.dump(config, f, indent=2, ensure_ascii=False)
            
            print_colored(f"MCP 설정 저장 완료: {self.mcp_json_path}", Colors.GREEN)
            return True
        except Exception as e:
            print_colored(f"MCP 설정 저장 오류: {str(e)}", Colors.FAIL)
            return False
    
    def get_mcp_command_args(self, base_args: List[str], command_type: str = 'default') -> tuple:
        """OS별 MCP 명령어와 인자 반환"""
        if OSInfo.is_windows():
            # Windows에서는 cmd /c npx ... 형태로 실행
            return 'cmd', ['/c', 'npx'] + base_args
        else:
            # macOS, Linux에서는 npx ... 형태로 실행
            return 'npx', base_args
    
    def add_mcp_server(self, name: str, command: str, args: List[str]) -> bool:
        """MCP 서버 추가"""
        config = self.load_mcp_config()
        
        # mcpServers 키가 없으면 생성
        if 'mcpServers' not in config:
            config['mcpServers'] = {}
        
        # OS별로 명령어와 인자 조정
        if command == "npx":
            if OSInfo.is_windows():
                command = 'cmd'
                args = ['/c', 'npx'] + args
        
        # 서버 설정 추가
        config['mcpServers'][name] = {
            'command': command,
            'args': args
        }
        
        return self.save_mcp_config(config)
    
    def remove_mcp_server(self, name: str) -> bool:
        """MCP 서버 제거"""
        config = self.load_mcp_config()
        
        if 'mcpServers' not in config or name not in config['mcpServers']:
            print_colored(f"MCP 서버를 찾을 수 없습니다: {name}", Colors.WARNING)
            return False
        
        # 서버 설정 제거
        del config['mcpServers'][name]
        
        return self.save_mcp_config(config)
    
    def export_mcp_config(self, output_path: Optional[str] = None) -> bool:
        """MCP 설정 내보내기"""
        config = self.load_mcp_config()
        
        if not config:
            print_colored("내보낼 MCP 설정이 없습니다.", Colors.WARNING)
            return False
        
        if output_path is None:
            output_path = self.target_dir / "exported_mcp_config.json"
        else:
            output_path = Path(output_path)
        
        try:
            with open(output_path, 'w', encoding='utf-8') as f:
                json.dump(config, f, indent=2, ensure_ascii=False)
            
            print_colored(f"MCP 설정 내보내기 완료: {output_path}", Colors.GREEN)
            return True
        except Exception as e:
            print_colored(f"MCP 설정 내보내기 오류: {str(e)}", Colors.FAIL)
            return False
    
    def import_mcp_config(self, input_path: str) -> bool:
        """MCP 설정 가져오기"""
        input_path = Path(input_path)
        
        if not input_path.exists():
            print_colored(f"가져올 MCP 설정 파일이 없습니다: {input_path}", Colors.WARNING)
            return False
        
        try:
            with open(input_path, 'r', encoding='utf-8') as f:
                config = json.load(f)
            
            # OS별 명령어 자동 변환
            if 'mcpServers' in config:
                for name, server in config['mcpServers'].items():
                    command = server.get('command', '')
                    args = server.get('args', [])
                    
                    # Windows와 다른 OS 사이의 명령어 변환
                    if OSInfo.is_windows() and command == "npx":
                        # 다른 OS 형식(npx)에서 Windows 형식(cmd /c npx)으로 변환
                        server['command'] = 'cmd'
                        server['args'] = ['/c', 'npx'] + args
                    elif not OSInfo.is_windows() and command == "cmd" and args and args[0] == "/c" and args[1] == "npx":
                        # Windows 형식(cmd /c npx)에서 다른 OS 형식(npx)으로 변환
                        server['command'] = 'npx'
                        server['args'] = args[2:]  # '/c'와 'npx' 제거
            
            return self.save_mcp_config(config)
        except json.JSONDecodeError:
            print_colored(f"MCP 설정 파일 파싱 오류: {input_path}", Colors.FAIL)
            return False
        except Exception as e:
            print_colored(f"MCP 설정 가져오기 오류: {str(e)}", Colors.FAIL)
            return False
    
    def setup_default_mcp_servers(self) -> bool:
        """기본 MCP 서버 설정"""
        # Node.js 설치 확인
        if not NodeJSChecker.is_nodejs_installed():
            print_colored("Node.js가 설치되어 있어야 합니다.", Colors.FAIL)
            return False
        
        # 백업 먼저 수행
        self.backup_mcp_config()
        
        config = self.load_mcp_config()
        
        if 'mcpServers' not in config:
            config['mcpServers'] = {}
        
        # 기본 인자 설정
        think_args = [
            '-y',
            '@smithery/cli@latest',
            'run',
            '@PhillipRt/think-mcp-server',
            '--key',
            'f120217f-d8f9-4b5e-b9c9-cf9feb0aad83'
        ]
        
        sequential_args = [
            '-y',
            '@smithery/cli@latest',
            'run',
            '@smithery-ai/server-sequential-thinking',
            '--key',
            'f120217f-d8f9-4b5e-b9c9-cf9feb0aad83'
        ]
        
        # OS별 명령어 설정
        if OSInfo.is_windows():
            # Windows에서는 cmd /c npx ... 형태로 실행
            think_cmd, think_full_args = 'cmd', ['/c', 'npx'] + think_args
            seq_cmd, seq_full_args = 'cmd', ['/c', 'npx'] + sequential_args
        else:
            # macOS, Linux에서는 npx ... 형태로 실행
            think_cmd, think_full_args = 'npx', think_args
            seq_cmd, seq_full_args = 'npx', sequential_args
        
        # Think MCP 서버 설정
        config['mcpServers']['think-mcp-server'] = {
            'command': think_cmd,
            'args': think_full_args
        }
        
        # Sequential Thinking 서버 설정
        config['mcpServers']['server-sequential-thinking'] = {
            'command': seq_cmd,
            'args': seq_full_args
        }
        
        result = self.save_mcp_config(config)
        if result:
            print_colored("기본 MCP 서버 설정 완료!", Colors.GREEN)
        
        return result
    
    def setup_github_mcp(self, token: str) -> bool:
        """GitHub MCP 설정"""
        # Node.js 설치 확인
        if not NodeJSChecker.is_nodejs_installed():
            print_colored("Node.js가 설치되어 있어야 합니다.", Colors.FAIL)
            return False
            
        if not token:
            print_colored("GitHub 토큰이 필요합니다.", Colors.WARNING)
            return False
        
        config = self.load_mcp_config()
        
        if 'mcpServers' not in config:
            config['mcpServers'] = {}
        
        # 기본 인자 설정
        github_args = [
            '-y',
            '@smithery/cli@latest',
            'run',
            '@smithery-ai/github',
            '--config',
            f'{{"githubPersonalAccessToken":"{token}"}}'
        ]
        
        # OS별 명령어 설정
        if OSInfo.is_windows():
            # Windows에서는 cmd /c npx ... 형태로 실행
            github_cmd, github_full_args = 'cmd', ['/c', 'npx'] + github_args
        else:
            # macOS, Linux에서는 npx ... 형태로 실행
            github_cmd, github_full_args = 'npx', github_args
        
        # GitHub MCP 서버 설정
        config['mcpServers']['github'] = {
            'command': github_cmd,
            'args': github_full_args
        }
        
        result = self.save_mcp_config(config)
        if result:
            print_colored("GitHub MCP 서버 설정 완료!", Colors.GREEN)
        
        return result
    
    def setup_all(self, github_token=None):
        """모든 MCP 설정"""
        # Node.js 설치 확인
        if not NodeJSChecker.is_nodejs_installed():
            print_colored("Node.js가 설치되어 있어야 합니다.", Colors.FAIL)
            return False
            
        # MCP 설치
        installer = MCPInstaller()
        install_success = installer.install_all_mcps(github_token)
        
        if not install_success:
            print_colored("MCP 설치 중 문제가 발생했습니다.", Colors.WARNING)
            # 설치 문제가 있어도 설정은 진행
        
        # 기본 MCP 서버 설정
        setup_success = self.setup_default_mcp_servers()
        
        # GitHub MCP 서버 설정 (토큰이 제공된 경우)
        if github_token and setup_success:
            self.setup_github_mcp(github_token)
        
        return setup_success
        
    def list_mcp_servers(self) -> None:
        """MCP 서버 목록 출력"""
        config = self.load_mcp_config()
        
        if 'mcpServers' not in config or not config['mcpServers']:
            print_colored("설정된 MCP 서버가 없습니다.", Colors.WARNING)
            return
        
        print_colored("\n===== MCP 서버 목록 =====", Colors.HEADER)
        for name, server in config['mcpServers'].items():
            print_colored(f"\n[{name}]", Colors.BOLD)
            print(f"  명령어: {server.get('command', 'N/A')}")
            print(f"  인자: {' '.join(server.get('args', []))}")
        
        print_colored("\n========================", Colors.HEADER)
    
    def show_os_info(self) -> None:
        """OS 정보 표시"""
        os_details = OSInfo.get_os_details()
        
        print_colored("\n===== 시스템 정보 =====", Colors.HEADER)
        print(f"운영 체제: {os_details['system']}")
        print(f"버전: {os_details['release']} ({os_details['version']})")
        print(f"아키텍처: {os_details['machine']}")
        print(f"프로세서: {os_details['processor']}")
        print(f"Python 버전: {os_details['python_version']}")
        
        # Node.js 정보 표시
        node_installed = NodeJSChecker.is_nodejs_installed()
        node_version = NodeJSChecker.get_nodejs_version() if node_installed else "설치되지 않음"
        print(f"Node.js 설치 여부: {node_installed}")
        print(f"Node.js 버전: {node_version}")
        
        print(f"Cursor 설정 경로: {self.cursor_dir}")
        print(f"MCP 설정 파일: {self.mcp_json_path}")
        print_colored("========================", Colors.HEADER)

def setup_argument_parser():
    """명령행 인자 파서 설정"""
    parser = argparse.ArgumentParser(description='MCP 설정 도구')
    subparsers = parser.add_subparsers(dest='command', help='명령')
    
    # 기본 설정 명령
    subparsers.add_parser('setup', help='기본 MCP 서버 설정')
    
    # GitHub 설정 명령
    github_parser = subparsers.add_parser('github', help='GitHub MCP 설정')
    github_parser.add_argument('--token', required=True, help='GitHub 개인 액세스 토큰')
    
    # 서버 추가 명령
    add_parser = subparsers.add_parser('add', help='MCP 서버 추가')
    add_parser.add_argument('--name', required=True, help='서버 이름')
    add_parser.add_argument('--command', required=True, help='실행 명령어')
    add_parser.add_argument('--args', required=True, help='명령어 인자 (쉼표로 구분)')
    
    # 서버 제거 명령
    remove_parser = subparsers.add_parser('remove', help='MCP 서버 제거')
    remove_parser.add_argument('--name', required=True, help='서버 이름')
    
    # 설정 내보내기 명령
    export_parser = subparsers.add_parser('export', help='MCP 설정 내보내기')
    export_parser.add_argument('--output', help='출력 파일 경로')
    
    # 설정 가져오기 명령
    import_parser = subparsers.add_parser('import', help='MCP 설정 가져오기')
    import_parser.add_argument('--input', required=True, help='입력 파일 경로')
    
    # 서버 목록 명령
    subparsers.add_parser('list', help='MCP 서버 목록 출력')
    
    # 백업 명령
    subparsers.add_parser('backup', help='MCP 설정 백업')
    
    # 시스템 정보 명령
    subparsers.add_parser('sysinfo', help='시스템 정보 표시')
    
    # MCP 설치 명령
    install_parser = subparsers.add_parser('install', help='MCP 설치')
    install_parser.add_argument('--github-token', help='GitHub MCP 설치에 사용할 토큰')
    
    # 모든 설정 명령 (설치 + 설정)
    all_parser = subparsers.add_parser('all', help='MCP 설치 및 설정 모두 수행')
    all_parser.add_argument('--github-token', help='GitHub MCP 설치 및 설정에 사용할 토큰')
    
    return parser

def main():
    """메인 함수"""
    parser = setup_argument_parser()
    args = parser.parse_args()
    
    mcp_setup = MCPSetup()
    
    if args.command == 'setup':
        mcp_setup.setup_default_mcp_servers()
    
    elif args.command == 'github':
        mcp_setup.setup_github_mcp(args.token)
    
    elif args.command == 'add':
        mcp_setup.add_mcp_server(
            args.name,
            args.command,
            args.args.split(',')
        )
    
    elif args.command == 'remove':
        mcp_setup.remove_mcp_server(args.name)
    
    elif args.command == 'export':
        mcp_setup.export_mcp_config(args.output)
    
    elif args.command == 'import':
        mcp_setup.import_mcp_config(args.input)
    
    elif args.command == 'list':
        mcp_setup.list_mcp_servers()
    
    elif args.command == 'backup':
        mcp_setup.backup_mcp_config()
    
    elif args.command == 'sysinfo':
        mcp_setup.show_os_info()
        
    elif args.command == 'install':
        if not NodeJSChecker.is_nodejs_installed():
            print_colored("Node.js가 설치되어 있어야 합니다.", Colors.FAIL)
            return
        
        installer = MCPInstaller()
        installer.install_all_mcps(args.github_token)
        
    elif args.command == 'all':
        mcp_setup.setup_all(args.github_token)
    
    else:
        print_colored("사용법: python mcp_setup.py {setup|github|add|remove|export|import|list|backup|sysinfo|install|all}", Colors.WARNING)
        parser.print_help()

if __name__ == '__main__':
    main() 