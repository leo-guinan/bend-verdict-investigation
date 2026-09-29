import Base

type EmptyX is Data:

def shape(tag: Bool) -> Type:
  match tag:
    case False{}: EmptyX
    case True{}: Array<U32>

def read(-tag: Bool, value: shape(tag)) -> U32:
  match tag:
    case False{}:
      match value:
    case True{}:
      match value:
        case ALeaf{v}: v
        case ANode{l, r}: 0

def main() -> U32:
  read(False{}, ALeaf{7})
