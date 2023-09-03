"""creacion de la tabla producto y categorias

Revision ID: f0c1037e2b6a
Revises: 6178463361c1
Create Date: 2023-08-24 15:18:13.820229

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'f0c1037e2b6a'
down_revision = '6178463361c1'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('categorias',
    sa.Column('id', sa.Integer(), autoincrement=True, nullable=False),
    sa.Column('nombre', sa.Text(), nullable=True),
    sa.Column('fecha_creacion', sa.DateTime(), nullable=True),
    sa.Column('imagen', sa.Text(), nullable=True),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('productos',
    sa.Column('id', sa.Integer(), autoincrement=True, nullable=False),
    sa.Column('nombre', sa.Text(), nullable=False),
    sa.Column('descripcion', sa.Text(), nullable=True),
    sa.Column('precio', sa.Float(), nullable=False),
    sa.Column('imagen', sa.Text(), nullable=True),
    sa.Column('disponibilidad', sa.Boolean(), nullable=True),
    sa.Column('stock', sa.Integer(), nullable=False),
    sa.Column('categoria_id', sa.Integer(), nullable=True),
    sa.ForeignKeyConstraint(['categoria_id'], ['categorias.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('productos')
    op.drop_table('categorias')
    # ### end Alembic commands ###
