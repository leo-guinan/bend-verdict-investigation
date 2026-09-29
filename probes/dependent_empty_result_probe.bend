import Base

type N is Data:
  Z{}
  S{p: N}

type EmptyX is Data:

def Out(n: N) -> Type:
  match n:
    case Z{}: EmptyX
    case S{p}: N

def use(~F: @a: N -> @b: N -> {a == b : N} -> Out(a), a: N, b: N, e: {a == b : N}) -> Out(a):
  F(a,b,e)

def main() -> N:
  Z{}
