#--------------------------------------------------------------------------------
# 참조 모듈 목록.
#--------------------------------------------------------------------------------
from __future__ import annotations
from typing import Awaitable, Callable, Final, Generic, Iterable, Iterator, Optional, Sequence, Type, TypeVar, Tuple, Union
from typing import ItemsView, KeysView, ValuesView
from typing import IO, TextIO, BinaryIO
from typing import Any, List, Dict, Set
from typing import cast, overload
from .directory import Directory


#--------------------------------------------------------------------------------
# 프레그먼트 요소.
#--------------------------------------------------------------------------------
class Fragment:
	#--------------------------------------------------------------------------------
	# 멤버 변수 목록.
	#--------------------------------------------------------------------------------
	Children: Optional[List[Component, ComponentRef, ComponentGroup, CreateFolder, Directory, DirectoryRef]]