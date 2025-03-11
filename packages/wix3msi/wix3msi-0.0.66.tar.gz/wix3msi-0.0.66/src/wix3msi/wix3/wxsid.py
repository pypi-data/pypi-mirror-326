#--------------------------------------------------------------------------------
# 참조 모듈 목록.
#--------------------------------------------------------------------------------
from __future__ import annotations
from typing import Awaitable, Callable, Final, Generic, Iterable, Iterator, Optional, Sequence, Type, TypeVar, Tuple, Union
from typing import ItemsView, KeysView, ValuesView
from typing import IO, TextIO, BinaryIO
from typing import Any, List, Dict, Set
from typing import cast, overload
import builtins
import re
from uuid import UUID
from uuid import uuid4 as CreateUUID


#--------------------------------------------------------------------------------
# 전역 상수 목록.
#--------------------------------------------------------------------------------
FILE_READTEXT: str = "rt"
FILE_WRITETEXT: str = "wt"
UTF8: str = "utf-8"
EMPTY: str = ""
SPACE: str = " "
UNDERSCORE: str = "_"
TAP: str = "\t"
LINEFEED: str = "\n"
RE_LOWERALPHABET_UPPERALPHABET_NUMBER_UNDERSCORE: str = "[^A-Za-z0-9_]"
RE_UPPERALPHABET_NUMBER_UNDERSCORE: str = "[^A-Z0-9_]"
RE_CONTINUOUS_UNDERSCORES: str = "_+"


#--------------------------------------------------------------------------------
# WXS 고유 식별자.
# - WXS ID는 72글자 이하의 영어대소문자, 숫자, 언더바만을 허용한다.
# - WXS ID는 중복되어서는 안된다.
#--------------------------------------------------------------------------------
class WXSID:
	#--------------------------------------------------------------------------------
	# 멤버 변수 목록.
	#--------------------------------------------------------------------------------
	__directories: Dict[str, str]
	__files: Dict[str, str]
	__componentGroups: Dict[str, str]
	__components: Dict[str, str]


	#--------------------------------------------------------------------------------
	# 초기화 라이프사이클 메서드.
	#--------------------------------------------------------------------------------
	def __init__(thisInstance) -> None:
		base = super()
		base.__init__()

		thisInstance.__directories = dict()
		thisInstance.__files = dict()
		thisInstance.__componentGroups = dict()
		thisInstance.__components = dict()


	#--------------------------------------------------------------------------------
	# 클리어.
	#--------------------------------------------------------------------------------
	def Clear(thisInstance) -> None:
		thisInstance.__directories.clear()
		thisInstance.__files.clear()
		thisInstance.__componentGroups.clear()
		thisInstance.__components.clear()


	#--------------------------------------------------------------------------------
	# 디렉토리 아이디 생성.
	#--------------------------------------------------------------------------------
	def CreateDirectoryID(thisInstance, targetPath: str) -> str:
		if targetPath in thisInstance.__directories:
			wxsID: str = thisInstance.__directories[targetPath]
			return wxsID
		else:
			wxsID: str = WXSID.CreateID(targetPath, "D")
			thisInstance.__directories[targetPath] = wxsID
			return wxsID


	#--------------------------------------------------------------------------------
	# 파일 아이디 생성.
	#--------------------------------------------------------------------------------
	def CreateFileID(thisInstance, targetFilePath: str) -> str:
		if targetFilePath in thisInstance.__files:
			wxsID: str = thisInstance.__files[targetFilePath]
			return wxsID
		else:
			guid: str = WXSID.CreateGUID()
			# wxsID: str = WXSIdentifierCacher.CreateWXSID(targetFilePath)
			wxsID: str = WXSID.CreateID(guid, "F")
			thisInstance.__files[targetFilePath] = wxsID
			return wxsID


	#--------------------------------------------------------------------------------
	# 컴포넌트 그룹 아이디 생성.
	#--------------------------------------------------------------------------------
	def CreateComponentGroupID(thisInstance, text: str) -> str:
		if text in thisInstance.__componentGroups:
			wxsID: str = thisInstance.__componentGroups[text]
			return wxsID
		else:
			wxsID: str = WXSID.CreateID(text, "CG")
			thisInstance.__componentGroups[text] = wxsID
			return wxsID
		

	#--------------------------------------------------------------------------------
	# 컴포넌트 아이디 생성.
	#--------------------------------------------------------------------------------
	def CreateComponentID(thisInstance, text: str) -> str:
		if text in thisInstance.__components:
			wxsID: str = thisInstance.__components[text]
			return wxsID
		else:
			wxsID: str = WXSID.CreateID(text, "C")
			thisInstance.__components[text] = wxsID
			return wxsID


	#--------------------------------------------------------------------------------
	# WXS ID 생성.
	#--------------------------------------------------------------------------------
	@staticmethod
	def Filter(text: str, useLowerAlphabet: bool = False) -> str:

		# 입력된 글자가 없는 경우.
		if not text:
			raise ValueError(f"[wix3msi] text is None")

		# 소문자를 사용하지 않을 경우 강제 대문자 변환.
		if not useLowerAlphabet:
			text = text.upper()

		# 대소문자알파벳, 숫자, 언더바만 유지하고 그 외의 모든 문자는 전부 언더바로 변환.
		text = re.sub(RE_LOWERALPHABET_UPPERALPHABET_NUMBER_UNDERSCORE, UNDERSCORE, text)

		# 언더바가 연속적으로 붙어서 나열되어 있을 때, 이를 하나의 언더바로 통합. (___ => _)
		text = re.sub(RE_CONTINUOUS_UNDERSCORES, UNDERSCORE, text)

		# 문자열의 시작과 끝에 언더바가 있다면 이를 제거.
		text = text.strip(UNDERSCORE)

		# 입력된 글자가 없는 경우.
		if builtins.len(text) < 1:
			raise ValueError(f"[wix3msi] Standard identifiers must be at least 1 character long. ('{text}')")

		# 72글자 제한에 걸릴 경우.
		if builtins.len(text) > 72:
			raise ValueError(f"[wix3msi] Standard identifiers are 72 characters long or less. ('{text}')")

		return text
	

	#--------------------------------------------------------------------------------
	# WXS의 Id에 들어갈 수 있는 문자열 포맷에 맞도록 입력 문자열을 수정하여 반환.
	# - 필요시 접두어를 붙일 수 있음.
	#--------------------------------------------------------------------------------
	@staticmethod
	def CreateID(text: str, prefix: str = None) -> str:
		text = WXSID.Filter(text, False)
		if prefix:
			prefix = WXSID.Filter(prefix)
			text = f"{prefix}_{text}"
		return text


	#--------------------------------------------------------------------------------
	# WXS GUID 생성.
	# - 1. UUID 생성. (GUID와 글자 수가 동일)
	# - 2. 소문자 알파벳을 대문자 알파벳으로 변경.
	# - 3. UUID에 포함된 공백, 중괄호, 하이픈 WXS 기준에 맞지 않는 문자 전체 제거.

	#--------------------------------------------------------------------------------
	@staticmethod
	def CreateGUID() -> str:
		uuid: UUID = CreateUUID()
		guid: str = str(uuid)
		guid = WXSID.Filter(guid)
		return guid