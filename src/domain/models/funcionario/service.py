class FuncionarioService:
    def get_funcionario_by_id(self, id: int, session: AsyncSession):
        result = session.execute(
            select(Funcionario).where(Funcionario.id == id))
        return result.scalars().first()
