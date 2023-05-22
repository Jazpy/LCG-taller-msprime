import numpy as np
import msprime


########################
# EJERCICIOS ANCESTRIA #
########################


def poblacion_simple():
  '''
  Simulación de 10 muestras diploides, una sola población constante.

  Valor de salida:
    Secuencia de árboles resultante de msprime.sim_ancestry().

  Documentación relevante:
    msprime.sim_ancestry()
  '''
  arboles = msprime.sim_ancestry(samples=10, ploidy=2,
    population_size=10_000)

  return arboles


def cuello_de_botella():
  '''
  Simulación de 10 muestras diploides, una sola población llamada "A" que:
    En el tiempo 0 tiene un tamaño de población efectivo = 1,000
    20 generaciones en el pasado tiene N_e = 10,000

  El modelo demográfico debe especificarse a través de msprime.Demography.

  Valor de salida:
    Tupla de la forma (secuencia de árboles, modelo demográfico).

  Documentación relevante:
    msprime.Demography
    msprime.sim_ancestry()
  '''
  modelo_dem = msprime.Demography()
  modelo_dem.add_population(name='A', initial_size=1_000)
  modelo_dem.add_population_parameters_change(time=20,
    population='A', initial_size=10_000)

  arboles = msprime.sim_ancestry(samples=10, ploidy=2, demography=modelo_dem)

  return (arboles, modelo_dem)


def divergencia_simple():
  '''
  Simulación de 5 muestras diploides de cada población,
  se consideran dos poblaciones "A" y "B" que:
    Tienen N_e = 10,000 en el presente.
    Se vuelven una sola población "C" 100 generaciones en el pasado.
    "C" tiene N_e = 5,000

  Las caracteristícas de las muestras deben especificarse a través
  de un objeto msprime.SampleSet.

  Valor de salida:
    Tupla de la forma (secuencia de árboles, modelo demográfico).

  Documentación relevante:
    msprime.Demography
    msprime.SampleSet
    msprime.sim_ancestry()
  '''
  modelo_dem = msprime.Demography()
  modelo_dem.add_population(name='A', initial_size=10_000)
  modelo_dem.add_population(name='B', initial_size=10_000)
  modelo_dem.add_population(name='C', initial_size=5_000)
  modelo_dem.add_population_split(time=100, derived=['A', 'B'], ancestral='C')

  muestras_a = msprime.SampleSet(5, population='A', time=0, ploidy=2)
  muestras_b = msprime.SampleSet(5, population='B', time=0, ploidy=2)

  arboles = msprime.sim_ancestry(samples=[muestras_a, muestras_b],
    demography=modelo_dem)

  return (arboles, modelo_dem)


def admixture_simple():
  '''
  Simulación de 10 muestras disploides de una población llamada "ADMIXED",
  la población "ADMIXED" debe:
    Estar conformada por 3 poblaciones "A", "B", y "C".
    Las proporciones de estas poblaciones deben ser 0.5, 0.3, y 0.2
    El edvento de admixture ocurrió 20 generaciones en el pasado.

  "A", "B", y "C" se unen en una población "ANC", hace 1,000 generaciones
  Todas las poblaciones deben tener N_e = 10,000

  Valor de salida:
    Tupla de la forma (secuencia de árboles, modelo demográfico).

  Documentación relevante:
    msprime.Demography
    msprime.SampleSet
    msprime.sim_ancestry()
  '''
  modelo_dem = msprime.Demography()
  modelo_dem.add_population(name='A',       initial_size=10_000)
  modelo_dem.add_population(name='B',       initial_size=10_000)
  modelo_dem.add_population(name='C',       initial_size=10_000)
  modelo_dem.add_population(name='ADMIXED', initial_size=10_000)
  modelo_dem.add_population(name='ANC',     initial_size=10_000)
  modelo_dem.add_admixture(time=20, derived='ADMIXED',
    ancestral=['A', 'B', 'C'], proportions=[0.5, 0.3, 0.2])
  modelo_dem.add_population_split(time=1_000, derived=['A', 'B', 'C'],
    ancestral='ANC')

  muestras = msprime.SampleSet(10, population='ADMIXED', time=0, ploidy=2)

  arboles = msprime.sim_ancestry(samples=[muestras],
    demography=modelo_dem)

  return (arboles, modelo_dem)


#########################
# EJERCICIOS MUTACIONES #
#########################


def generar_modelo_aux(num_muestras):
  '''
  Función auxiliar para generar un modelo demográfico y especificación
  de muestras que pueden ser utilizados por msprime.sim_ancestry().

  Valor de entrada:
    num_muestras: Número de haplotipos a generar para cada población.

  Valor de salida:
    Tupla de la forma (modelo demografico, lista de descripción de muestras).

  Documentación relevante:
    msprime.Demography
    msprime.SampleSet
  '''
  modelo_dem = msprime.Demography()
  modelo_dem.add_population(name='A',   initial_size=10_000)
  modelo_dem.add_population(name='B',   initial_size=10_000)
  modelo_dem.add_population(name='C',   initial_size=10_000)
  modelo_dem.add_population(name='AB',  initial_size=10_000)
  modelo_dem.add_population(name='ABC', initial_size=10_000)
  modelo_dem.add_population_split(time=50, derived=['A', 'B'],
    ancestral='AB')
  modelo_dem.add_population_split(time=200, derived=['AB', 'C'],
    ancestral='ABC')

  muestras_a = msprime.SampleSet(num_muestras,
    population='A', time=0, ploidy=1)
  muestras_b = msprime.SampleSet(num_muestras,
    population='B', time=0, ploidy=1)
  muestras_c = msprime.SampleSet(num_muestras,
    population='C', time=0, ploidy=1)
  muestras   = [muestras_a, muestras_b, muestras_c]

  return (modelo_dem, muestras)


def sim_mutaciones():
  '''
  Simulación del modelo descrito en la función generar_modelo_aux().
  Se deben simular 20 muestras por población, esto se especifica como
  parámetro de generar_modelo_aux().
  La simulación debe tener los siguientes parámetros:
    Longitud de la secuencia = 10,000
    Tasa de recombinación    = 2e-08
    Tasa de mutación         = 2e-08

  Valor de salida:
    Secuencia de árboles después de simular mutaciones.

  Documentación relevante:
    msprime.sim_ancestry()
    msprime.sim_mutations()
  '''
  modelo, muestras = generar_modelo_aux(20)
  arboles = msprime.sim_ancestry(samples=muestras,
    demography=modelo, recombination_rate=2e-08,
    sequence_length=10_000)
  arboles = msprime.sim_mutations(arboles, rate=2e-08)

  return arboles


def variante_comun(arboles):
  '''
  Dada una secuencia de árboles, encuentra la variante más común.

  Valor de entrada:
    arboles: Secuencia de árboles resultante de msprime.sim_mutations()

  Valor de salida:
    Número de haplotipos que cuentan con la variante más común.

  Documentación relevante:
    tskit.TreeSequence
    tskit.TreeSequence.variants()
    tskit.Variant
  '''
  maximo = 0
  for v in arboles.variants():
    maximo = max(np.count_nonzero(v.genotypes), maximo)

  return maximo


def variante_rara(arboles):
  '''
  Dada una secuencia de árboles, encuentra la variante más rara.

  Valor de entrada:
    arboles: Secuencia de árboles resultante de msprime.sim_mutations()

  Valor de salida:
    Número de haplotipos que cuentan con la variante más rara.

  Documentación relevante:
    tskit.TreeSequence
    tskit.TreeSequence.variants()
    tskit.Variant
  '''
  minimo = np.Inf
  for v in arboles.variants():
    minimo = min(np.count_nonzero(v.genotypes), minimo)

  return minimo


def haplotipo_mutado(arboles):
  '''
  Dada una secuencia de árboles, encuentra el haplotipo con más variantes.

  Valor de entrada:
    arboles: Secuencia de árboles resultante de msprime.sim_mutations()

  Valor de salida:
    Haplotipo con más variantes, expresado como una cadena de 1s y 0s, sin
    ningún espacio u otros caracteres.

  Documentación relevante:
    tskit.TreeSequence
    tskit.TreeSequence.genotype_matrix()
  '''
  maximo = 0
  haplo  = None
  for h in arboles.genotype_matrix():
    cuenta = np.count_nonzero(h==1)
    if cuenta > maximo:
      haplo  = h
      maximo = cuenta

  return ''.join(str(x) for x in haplo)


def haplotipo_conservado(arboles):
  '''
  Dada una secuencia de árboles, encuentra el haplotipo con menos variantes.

  Valor de entrada:
    arboles: Secuencia de árboles resultante de msprime.sim_mutations()

  Valor de salida:
    Haplotipo con menos variantes, expresado como una cadena de 1s y 0s, sin
    ningún espacio u otros caracteres.

  Documentación relevante:
    tskit.TreeSequence
    tskit.TreeSequence.genotype_matrix()
  '''
  maximo = 0
  haplo  = None
  for h in arboles.genotype_matrix():
    cuenta = np.count_nonzero(h==0)
    if cuenta > maximo:
      haplo  = h
      maximo = cuenta

  return ''.join(str(x) for x in haplo)


def arbol_max(arboles):
  '''
  Dada una secuencia de árboles, encuentra el arbol que cubre la región
  genómica más larga.

  Valor de entrada:
    arboles: Secuencia de árboles resultante de msprime.sim_mutations()

  Valor de salida:
    Longitud del genoma que cubre el árbol más largo

  Documentación relevante:
    tskit.TreeSequence
    tskit.TreeSequence.trees()
    tskit.Tree
  '''
  return max([t.span for t in arboles.trees()])


def gnn(arbol, n, p):
  '''
  Encuentra los nodos genealógicamente más cercanas a un nodo n.

  Valores de entrada:
    arbol: Un solo árbol resultante de msprime.sim_mutations(), tskit.Tree
    n: nodo de referencia para encontrar vecinos más cercanos
    p: nodo padre de n

  Valor de salida:
    Lista ordenada con los IDs de los nodos genealógicamente más cercanos.

  Documentación relevante:
    https://youtu.be/YrZTKjLzZY0?t=2788
    tskit.Tree
    tskit.Tree.parent
    tskit.Tree.children
  '''
  pila  = list(arbol.children(p))
  gnn   = []

  while pila:
    nodo = pila.pop()

    if nodo == n:
      continue

    hijos = arbol.children(nodo)

    if not hijos:
      gnn.append(nodo)
    else:
      pila += hijos

  if gnn:
    return sorted(gnn)
  else:
    return gnn(arbol, n, arbol.parent(p))
