import Base

def F(~A: Type, ~B: @x: A -> Type) -> @x: A -> Type:
  B

def main() -> @x: Nat -> Type:
  F(~Nat, ~(x => Nat))
