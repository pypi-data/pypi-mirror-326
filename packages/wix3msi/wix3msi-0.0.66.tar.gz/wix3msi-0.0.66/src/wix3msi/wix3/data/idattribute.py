#--------------------------------------------------------------------------------
# 참조 모듈 목록.
#--------------------------------------------------------------------------------
from __future__ import annotations
from typing import Awaitable, Callable, Final, Generic, Iterable, Iterator, Optional, Sequence, Type, TypeVar, Tuple, Union
from typing import ItemsView, KeysView, ValuesView
from typing import IO, TextIO, BinaryIO
from typing import Any, List, Dict, Set
from typing import cast, overload


#--------------------------------------------------------------------------------
# 식별자 속성.
# - 태그의 속성으로 영어대소문자, 숫자, 언더바로만 이루어진 고유식별자 문자열을 의미.
#--------------------------------------------------------------------------------
class IdAttribute:
	#--------------------------------------------------------------------------------
	# 멤버 변수 목록.
	#--------------------------------------------------------------------------------
	Value: str

	#--------------------------------------------------------------------------------
	# 문자열 변환 오퍼레이터.
	#--------------------------------------------------------------------------------
	def __str__(thisInstance) -> str:
		return thisInstance.Value