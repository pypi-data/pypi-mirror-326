from typing import Generic, Hashable, Self, TypeVar, TYPE_CHECKING
from collections.abc import Iterable
from dataclasses import dataclass, replace
from inspect import signature
from .util.dataclasses import repr_default


if TYPE_CHECKING:
    from .node import Node


NodeData = TypeVar("NodeData", bound=Hashable)
EdgeData = TypeVar("EdgeData", bound=Hashable)


@repr_default
@dataclass(frozen=True, slots=True)
class Zipper(Generic[NodeData, EdgeData]):
    # Currently pointed node
    node: "Node[NodeData, EdgeData] | None" = None

    # Data attached to the incoming edge
    data: EdgeData | None = None

    # Child index into the parent node
    index: int = -1

    # Current depth level
    depth: int = 0

    # Parent pointer, or None if at root
    parent: "Zipper[NodeData, EdgeData] | None" = None

    def replace(self, **kwargs) -> Self:
        """
        Create a copy of the current cursor in which the attributes given
        as keyword arguments are replaced with the specified value.

        Values which are callables are invoked with the current cursor
        to compute the actual value used for replacement.
        """
        for key, value in kwargs.items():
            if callable(value):
                kwargs[key] = value(getattr(self, key))

        return replace(self, **kwargs)

    def is_empty(self) -> bool:
        """Test whether there is a pointed node."""
        return self.node is None

    def is_leaf(self) -> bool:
        """Test whether the pointed node is a leaf node."""
        return self.node is None or self.node.edges == ()

    def down(self, index: int = 0) -> "Zipper[NodeData, EdgeData]":
        """
        Move to a child of the pointed node.

        :param index: index of the child to move to;
            negative indices are supported (default: first child)
        :returns: updated zipper
        """
        if self.node is None or index >= len(self.node.edges):
            raise IndexError("child index out of range")

        edges = self.node.edges
        index %= len(edges)
        return self.replace(
            node=edges[index].node,
            data=edges[index].data,
            parent=self.replace(node=self.node.pop(index)),
            index=index,
            depth=self.depth + 1,
        )

    def children(self) -> "Iterable[Zipper[NodeData, EdgeData]]":
        """Iterate through each child of the pointed node."""
        if self.node is None:
            return ()

        return (self.down(index) for index in range(len(self.node.edges)))

    def root(self) -> "Iterable[Zipper[NodeData, EdgeData]]":
        """
        Reconfigure the tree so that the pointed node is the root.

        All nodes, edges and their attached data are preserved. The relative
        node ordering is also preserved. The original tree can be restored
        by re-rooting on the old root node.
        """
        if self.is_root():
            return self

        parent = self.parent.root().node
        parent = parent.replace(
            edges=parent.edges[self.index :] + parent.edges[: self.index]
        )

        return self.replace(
            node=self.node.add(parent, data=self.data),
            data=None,
            index=-1,
            depth=0,
            parent=None,
        )

    def is_root(self) -> bool:
        """Test whether the pointed node is a root node."""
        return self.parent is None

    def up(self) -> "Zipper[NodeData, EdgeData]":
        """Move to the parent of the pointed node."""
        if self.parent is None:
            raise IndexError("cannot go up")

        if self.node is None:
            return self.parent

        if self.parent.node is None:
            raise ValueError("cannot attach to empty parent zipper")

        return self.parent.replace(
            node=self.parent.node.add(self.node, data=self.data, index=self.index),
        )

    def is_last_sibling(self, direction: int = 1) -> bool:
        """
        Test whether the pointed node is the last sibling in a direction.

        :param direction: positive number to test in left to right order,
            negative number to test in right to left order
        """
        if self.parent is None or self.parent.node is None:
            return True

        if direction == 0:
            return False

        if direction < 0:
            return self.index == 0

        return self.index == len(self.parent.node.edges)

    def sibling(self, offset: int = 1) -> "Zipper[NodeData, EdgeData]":
        """
        Move to a sibling of the pointed node.

        :param offset: sibling offset relative to the current node;
            zero for self, positive for right, negative for left, wrapping
            around the child list if needed (default: sibling to the right)
        :returns: updated zipper
        """
        if self.parent is None or self.parent.node is None or offset == 0:
            return self

        if self.is_empty():
            offset -= 1

        index = self.index + offset
        index %= len(self.parent.node.edges) + 1
        return self.up().down(index)

    def _preorder(self, flip: bool) -> "Zipper[NodeData, EdgeData]":
        child = -1 if flip else 0
        sibling = -1 if flip else 1

        if not self.is_leaf():
            return self.down(child)

        while self.is_last_sibling(sibling):
            if self.is_root():
                return self

            self = self.up()

        return self.sibling(sibling)

    def _postorder(self, flip: bool) -> "Zipper[NodeData, EdgeData]":
        child = -1 if flip else 0
        sibling = -1 if flip else 1

        if self.is_root():
            while not self.is_leaf():
                self = self.down(child)

            return self

        if self.is_last_sibling(sibling):
            return self.up()

        self = self.sibling(sibling)

        while not self.is_leaf():
            self = self.down(child)

        return self

    def next(self, preorder: bool = False) -> "Zipper[NodeData, EdgeData]":
        """
        Move to the next node in preorder or postorder.

        :param preorder: pass True to move in preorder (default is postorder)
        :returns: updated zipper
        """
        if preorder:
            return self._preorder(flip=False)
        else:
            return self._postorder(flip=False)

    def prev(self, preorder: bool = False) -> "Zipper[NodeData, EdgeData]":
        """
        Move to the previous node in preorder or postorder.

        :param preorder: pass True to move in preorder (default is postorder)
        :returns: updated zipper
        """
        if preorder:
            return self._postorder(flip=True)
        else:
            return self._preorder(flip=True)

    def zip(self) -> "Node[NodeData, EdgeData] | None":
        """Zip up to the root and return it."""
        bubble = self

        while not bubble.is_root():
            bubble = bubble.up()

        return bubble.node

    def __str__(
        self,
        prefix: str = "",
        chars: dict[str, str] | None = None,
    ) -> str:
        tree = self.zip()

        if chars is None:
            chars = signature(tree.__str__).parameters["chars"].default

        return self.zip().__str__(prefix=prefix, chars=chars, highlight=self.node)
