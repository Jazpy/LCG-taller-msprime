import unittest
import soluciones as sol

from ejercicios import *


class PruebasUnitarias(unittest.TestCase):
  def test_caso_simple(self):
    arboles = poblacion_simple()

    # Obtener numero de muestras y poblaciones
    muestras    = arboles.num_samples
    poblaciones = arboles.num_populations

    self.assertEqual(muestras, 20)
    self.assertEqual(poblaciones, 1)


  def test_cuello_de_botella(self):
    arboles, modelo = cuello_de_botella()

    modelo_ref = msprime.Demography()
    modelo_ref.add_population(name='A', initial_size=1_000)
    modelo_ref.add_population_parameters_change(time=20,
      population='A', initial_size=10_000)

    self.assertTrue(modelo_ref.is_equivalent(modelo))
    self.assertEqual(arboles.num_samples, 20)
    self.assertEqual(arboles.num_populations, 1)


  def test_divergencia_simple(self):
    arboles, modelo = divergencia_simple()

    modelo_ref = msprime.Demography()
    modelo_ref.add_population(name='A', initial_size=10_000)
    modelo_ref.add_population(name='B', initial_size=10_000)
    modelo_ref.add_population(name='C', initial_size=5_000)
    modelo_ref.add_population_split(time=100, derived=['A', 'B'], ancestral='C')

    self.assertTrue(modelo_ref.is_equivalent(modelo))
    self.assertEqual(arboles.num_samples, 20)
    self.assertEqual(arboles.num_populations, 3)


  def test_admixture(self):
    arboles, modelo = admixture_simple()

    modelo_ref = msprime.Demography()
    modelo_ref.add_population(name='A',       initial_size=10_000)
    modelo_ref.add_population(name='B',       initial_size=10_000)
    modelo_ref.add_population(name='C',       initial_size=10_000)
    modelo_ref.add_population(name='ADMIXED', initial_size=10_000)
    modelo_ref.add_population(name='ANC',     initial_size=10_000)
    modelo_ref.add_admixture(time=20, derived='ADMIXED',
      ancestral=['A', 'B', 'C'], proportions=[0.5, 0.3, 0.2])
    modelo_ref.add_population_split(time=1_000, derived=['A', 'B', 'C'],
      ancestral='ANC')

    self.assertTrue(modelo_ref.is_equivalent(modelo))
    self.assertEqual(arboles.num_samples, 20)
    self.assertEqual(arboles.num_populations, 5)


  # Función local para simular árboles con mutaciones
  def __sim_mutado(self, n):
    modelo, muestras = generar_modelo_aux(n)
    arboles = msprime.sim_ancestry(samples=muestras,
      demography=modelo, recombination_rate=2e-08,
      sequence_length=10_000)

    return msprime.sim_mutations(arboles, rate=2e-08)


  def test_sim_mutaciones(self):
    arboles = sim_mutaciones()

    self.assertEqual(arboles.num_samples, 60)
    self.assertEqual(arboles.sequence_length, 10000.0)
    self.assertEqual(arboles.num_populations, 5)
    self.assertTrue(10 < arboles.num_trees < 90)
    self.assertTrue(10 < arboles.num_mutations < 90)


  def test_variantes(self):
    arboles = self.__sim_mutado(20)
    self.assertEqual(variante_comun(arboles), sol.variante_comun(arboles))
    self.assertEqual(variante_rara(arboles), sol.variante_rara(arboles))


  def test_haplotipos(self):
    arboles = self.__sim_mutado(20)
    self.assertEqual(haplotipo_mutado(arboles), sol.haplotipo_mutado(arboles))
    self.assertEqual(haplotipo_conservado(arboles),
      sol.haplotipo_conservado(arboles))


  def test_arbol(self):
    arboles = self.__sim_mutado(20)
    self.assertEqual(arbol_max(arboles), sol.arbol_max(arboles))


  def test_gnn(self):
    arboles = self.__sim_mutado(10)
    arbol   = arboles.at_index(0)

    n = 0
    self.assertEqual(gnn(arbol, n, arbol.parent(n)),
      sol.gnn(arbol, n, arbol.parent(n)))
    n = 15
    self.assertEqual(gnn(arbol, n, arbol.parent(n)),
      sol.gnn(arbol, n, arbol.parent(n)))
    n = 25
    self.assertEqual(gnn(arbol, n, arbol.parent(n)),
      sol.gnn(arbol, n, arbol.parent(n)))

if __name__ == '__main__':
  unittest.main()
