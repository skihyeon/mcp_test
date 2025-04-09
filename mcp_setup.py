#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
import json
import shutil
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

class MCPSetup:
    def __init__(self):
        self.home_dir = Path.home()
        self.cursor_dir = self.home_dir / '.cursor'
        self.mcp_json_path = self.cursor_dir / 'mcp.json'
        self.current_dir = Path.cwd()
        self.target_dir = self.current_dir / 'mcp_setup'
        self.backup_dir = self.target_dir / 'backups'
        
        # 필요한 디렉토리 생성
        self.backup_dir.mkdir(exist_ok=True, parents=True)
    
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
    
    def add_mcp_server(self, name: str, command: str, args: List[str]) -> bool:
        """MCP 서버 추가"""
        config = self.load_mcp_config()
        
        # mcpServers 키가 없으면 생성
        if 'mcpServers' not in config:
            config['mcpServers'] = {}
        
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
            
            return self.save_mcp_config(config)
        except json.JSONDecodeError:
            print_colored(f"MCP 설정 파일 파싱 오류: {input_path}", Colors.FAIL)
            return False
        except Exception as e:
            print_colored(f"MCP 설정 가져오기 오류: {str(e)}", Colors.FAIL)
            return False
    
    def setup_default_mcp_servers(self) -> bool:
        """기본 MCP 서버 설정"""
        # 백업 먼저 수행
        self.backup_mcp_config()
        
        config = self.load_mcp_config()
        
        if 'mcpServers' not in config:
            config['mcpServers'] = {}
        
        # Think MCP 서버 설정
        config['mcpServers']['think-mcp-server'] = {
            'command': 'npx',
            'args': [
                '-y',
                '@smithery/cli@latest',
                'run',
                '@PhillipRt/think-mcp-server',
                '--key',
                'f120217f-d8f9-4b5e-b9c9-cf9feb0aad83'
            ]
        }
        
        # Sequential Thinking 서버 설정
        config['mcpServers']['server-sequential-thinking'] = {
            'command': 'npx',
            'args': [
                '-y',
                '@smithery/cli@latest',
                'run',
                '@smithery-ai/server-sequential-thinking',
                '--key',
                'f120217f-d8f9-4b5e-b9c9-cf9feb0aad83'
            ]
        }
        
        result = self.save_mcp_config(config)
        if result:
            print_colored("기본 MCP 서버 설정 완료!", Colors.GREEN)
        
        return result
    
    def setup_github_mcp(self, token: str) -> bool:
        """GitHub MCP 설정"""
        if not token:
            print_colored("GitHub 토큰이 필요합니다.", Colors.WARNING)
            return False
        
        config = self.load_mcp_config()
        
        if 'mcpServers' not in config:
            config['mcpServers'] = {}
        
        # GitHub MCP 서버 설정
        config['mcpServers']['github'] = {
            'command': 'npx',
            'args': [
                '-y',
                '@smithery/cli@latest',
                'run',
                '@smithery-ai/github',
                '--config',
                f'{{"githubPersonalAccessToken":"{token}"}}'
            ]
        }
        
        result = self.save_mcp_config(config)
        if result:
            print_colored("GitHub MCP 서버 설정 완료!", Colors.GREEN)
        
        return result
    
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
    
    else:
        print_colored("사용법: python mcp_setup.py {setup|github|add|remove|export|import|list|backup}", Colors.WARNING)
        parser.print_help()

if __name__ == '__main__':
    main() 