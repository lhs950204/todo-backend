from dataclasses import dataclass
from typing import Any, Dict, Generic, List, Optional, Tuple, TypeVar, Union

from pydantic import BaseModel
from sqlalchemy import ColumnExpressionArgument, select, update
from sqlalchemy import delete as sql_delete
from sqlalchemy.orm import Session, joinedload, selectinload
from sqlalchemy.sql.elements import BinaryExpression

from app.models.base import ModelBase

T = TypeVar("T", bound=ModelBase)
CT = TypeVar("CT", bound=BaseModel | None)
UT = TypeVar("UT", bound=BaseModel | None)


@dataclass
class JoinInfo:
    """
    조인 작업에 필요한 정보를 담는 데이터 클래스
    """

    target: Any  # 조인 대상 모델
    condition: Optional[BinaryExpression] = None  # 조인 조건 (없으면 자동 외래키 관계 사용)
    isouter: bool = False  # 외부 조인 여부
    full: bool = False  # FULL OUTER JOIN 여부


class BaseRepository(Generic[T, CT, UT]):
    model: type[T]

    def __init_subclass__(cls) -> None:
        base = getattr(cls, "__orig_bases__", None)
        if base:
            base = base[0]
            if hasattr(base, "__args__"):
                _model = base.__args__[0]
                cls.model = _model
        return super().__init_subclass__()

    def __init__(self, session: Session):
        self.session = session

    async def create(self, create_data: CT) -> T:
        if create_data is None:
            raise ValueError("create_data is None")
        result = self.model(**create_data.model_dump())
        self.session.add(result)
        self.session.flush()
        return result

    async def update_one(self, id: int, update_data: UT) -> T:
        if update_data is None:
            raise ValueError("update_data is None")
        stmt = (
            update(self.model)
            .where(self.model.id == id)
            .values(**update_data.model_dump(exclude_unset=True))
            .returning(self.model)
        )
        result = self.session.scalar(stmt)
        if result is None:
            raise ValueError(f"{self.model.__name__} with id {id} not found")
        self.session.flush()
        return result

    async def find(
        self,
        *queries: ColumnExpressionArgument,
        joins: Optional[List[Union[Any, JoinInfo]]] = None,
        order_by: Optional[List[Any]] = None,
        limit: Optional[int] = None,
        offset: Optional[int] = None,
        options: Optional[List[Any]] = None,
        group_by: Optional[List[Any]] = None,
    ) -> List[T]:
        """
        쿼리를 실행하여 여러 항목을 찾습니다.

        Args:
            queries: WHERE 조건들
            joins: JOIN할 모델 목록 또는 JoinInfo 객체 목록
                  (예: [Model1, JoinInfo(Model2, Model1.id == Model2.model1_id, isouter=True)])
            order_by: 정렬 조건 목록 (예: [Model.column.asc(), Model.column2.desc()])
            limit: 반환할 최대 항목 수
            offset: 건너뛸 항목 수
            options: 추가 쿼리 옵션 (예: [selectinload(Model.relationship)])
            group_by: GROUP BY 조건 목록
        """
        stmt = select(self.model).where(*queries)

        # JOIN 적용
        if joins:
            for join in joins:
                if isinstance(join, JoinInfo):
                    stmt = stmt.join(join.target, join.condition, isouter=join.isouter, full=join.full)
                else:
                    stmt = stmt.join(join)

        # 정렬 적용
        if order_by:
            stmt = stmt.order_by(*order_by)

        # GROUP BY 적용
        if group_by:
            stmt = stmt.group_by(*group_by)

        # 페이지네이션 적용
        if limit is not None:
            stmt = stmt.limit(limit)
        if offset is not None:
            stmt = stmt.offset(offset)

        # 추가 옵션 적용
        if options:
            for option in options:
                stmt = stmt.options(option)

        result = self.session.scalars(stmt).all()
        return list(result)

    async def find_one(
        self,
        *queries: ColumnExpressionArgument,
        joins: Optional[List[Union[Any, JoinInfo]]] = None,
        order_by: Optional[List[Any]] = None,
        options: Optional[List[Any]] = None,
        group_by: Optional[List[Any]] = None,
    ) -> T:
        """
        쿼리를 실행하여 단일 항목을 찾습니다.

        Args:
            queries: WHERE 조건들
            joins: JOIN할 모델 목록 또는 JoinInfo 객체 목록
                  (예: [Model1, JoinInfo(Model2, Model1.id == Model2.model1_id, isouter=True)])
            order_by: 정렬 조건 목록 (예: [Model.column.asc(), Model.column2.desc()])
            options: 추가 쿼리 옵션 (예: [selectinload(Model.relationship)])
            group_by: GROUP BY 조건 목록
        """
        stmt = select(self.model).where(*queries)

        # JOIN 적용
        if joins:
            for join in joins:
                if isinstance(join, JoinInfo):
                    stmt = stmt.join(join.target, join.condition, isouter=join.isouter, full=join.full)
                else:
                    stmt = stmt.join(join)

        # 정렬 적용
        if order_by:
            stmt = stmt.order_by(*order_by)

        # GROUP BY 적용
        if group_by:
            stmt = stmt.group_by(*group_by)

        # 추가 옵션 적용
        if options:
            for option in options:
                stmt = stmt.options(option)

        result = self.session.scalar(stmt)
        if result is None:
            raise ValueError(f"{self.model.__name__} not found")
        return result

    async def delete(self, id: int) -> None:
        stmt = sql_delete(self.model).where(self.model.id == id)
        self.session.execute(stmt)
        self.session.flush()
