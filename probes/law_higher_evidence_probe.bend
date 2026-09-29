import Base

type N is Data:
  Z{}
  S{p: N}

law use:
  for ~F: @a: N -> @b: N -> {S{a} == S{b} : N} -> {a == b : N}
  for a: N
  for b: N
  for e: {S{a} == S{b} : N}
  {a == b : N}

def use(F, a, b, e):
  F(a, b, e)

def main() -> N:
  Z{}
