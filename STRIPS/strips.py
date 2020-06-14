class World:
    def __init__(self, monkey_pos, banana_pos, box_pos):
        self.monkey_pos = monkey_pos
        self.banana_pos = banana_pos
        self.box_pos = box_pos
        self.is_monkey_on_box = False
        self.bananas_picked = False

    # Metodo para verificar que la posicion indicada esta entre 1 y 3
    def is_inbounds(self, pos):
        return pos >= 1 and pos <= 3

    # Metodo utilizado para ver el estado en que se encuentra el mundo actualmente
    def print_state(self):
        print("El estado actual es:")
        print("El mono esta en la posicion", self.monkey_pos)
        print("Los platanos estan en la posicion", self.banana_pos)
        print("La caja esta en la posicion", self.box_pos)
        print("Esta el mono en la caja? " + str(self.is_monkey_on_box))
        print("Han sido cogidos los platanos? " + str(self.bananas_picked))

    # Funcion para mover el mono de posicion
    def move_monkey(self, dest_pos):
        if self.is_inbounds(dest_pos):
            if dest_pos is self.monkey_pos:
                print("El mono ya esta en esta posicion")
            self.monkey_pos = dest_pos
        else:
            print("Posicion incorrecta, prueba una posicion entre 1 y 3")

    # Funcion para empujar la caja
        # Solo funciona si el mono esta en la misma posicion que la caja
    def push_box(self, dest_pos):
        if self.is_inbounds(dest_pos):
            if dest_pos is self.box_pos:
                print("La caja ya esta en esta posicion")
            if self.monkey_pos is not self.box_pos:
                print("El mono y la caja deben estar en la misma posicion para poder empujarla")
            else:
                self.box_pos = dest_pos
        else:
            print("Posicion incorrecta, prueba una posicion entre 1 y 3")

    # Funcion para subirse a la caja
        #Solo funciona si el mono esta en la misma posicion que la caja
    def climb_box(self):
        if self.monkey_pos is self.box_pos and not self.is_monkey_on_box:
            self.is_monkey_on_box = True

    # Funcion para recoger las bananas
        # Solo funciona si el mono esta subido a la caja
    def pick_bananas(self):
        if self.is_monkey_on_box:
            self.bananas_picked = True


    '''
    Funcion para generar todos los estados posibles
    
    Por motivos de simplicidad, cuando el mono esta en la misma posicion que la caja los unicos movimientos posibles son los de empuajr la caja
    Tambien es posible que el mono no empuje la caja, pero ese escenario no lo he considerado porque no tiene sentido, seria como volver a un estado anterior
    Esto mismo hago tambien cuando el mono esta en la misma posicion que los platanos y la caja, su unico movimiento posible es el de subirse
    Al igual que cuando esta subido a la caja, su unico movimiento posible es el de recoger los platanos
    
    Durante este procedimiento, genero otro mundo donde se hace cada posible movimiento y calculo la meta que se ha conseguido haciendolo
    Al final se devuelve una lista con los posibles movimientos en cada estado y las metas conseguidas haciendo cada uno de ellos
    '''
    def generate_child(self, current_world):
        ret = []
        metas = []
        # Genero dos mundos alternativos, es necesario crearlos asi para evitar problemas de sobre escritura de memoria
        new_world1 = World(current_world.monkey_pos, current_world.banana_pos, current_world.box_pos)
        new_world1.is_monkey_on_box = current_world.is_monkey_on_box
        new_world1.bananas_picked = current_world.bananas_picked
        new_world2 = World(current_world.monkey_pos, current_world.banana_pos, current_world.box_pos)
        new_world2.is_monkey_on_box = current_world.is_monkey_on_box
        new_world2.bananas_picked = current_world.bananas_picked

        # El primer estado a tener en cuenta es cuando el mono y la caja estan en diferentes posiciones
        if not self.bananas_picked and self.monkey_pos is not self.box_pos and self.box_pos is not self.banana_pos and self.monkey_pos is not self.banana_pos:
            if self.monkey_pos == 1:
                new_world1.move_monkey(2)
                meta1 = self.meta_conseguida(new_world1)
                ret.append(new_world1)
                metas.append(meta1)
                new_world2.move_monkey(3)
                meta2 = self.meta_conseguida(new_world2)
                ret.append(new_world2)
                metas.append(meta2)
            elif self.monkey_pos == 2:
                new_world1.move_monkey(1)
                meta1 = self.meta_conseguida(new_world1)
                ret.append(new_world1)
                metas.append(meta1)
                new_world2.move_monkey(3)
                meta2 = self.meta_conseguida(new_world2)
                ret.append(new_world2)
                metas.append(meta2)
            else:
                self.move_monkey(1)
                meta1 = self.meta_conseguida(new_world1)
                ret.append(new_world1)
                metas.append(meta1)
                new_world2.move_monkey(2)
                meta2 = self.meta_conseguida(new_world2)
                ret.append(new_world2)
                metas.append(meta2)
            return ret, metas

        # Aqui estamos en el estado en que el mono y la caja estan en la misma posicion, y el mono procede a empujarla
        if not self.bananas_picked and self.monkey_pos is self.box_pos and not self.is_monkey_on_box and self.banana_pos is not self.box_pos:
            if self.monkey_pos == 1:
                new_world1.push_box(2)
                meta1 = self.meta_conseguida(new_world1)
                ret.append(new_world1)
                metas.append(meta1)
                new_world2.push_box(3)
                meta2 = self.meta_conseguida(new_world2)
                ret.append(new_world2)
                metas.append(meta2)
            elif self.monkey_pos == 2:
                new_world1.push_box(1)
                meta1 = self.meta_conseguida(new_world1)
                ret.append(new_world1)
                metas.append(meta1)
                new_world2.push_box(3)
                meta2 = self.meta_conseguida(new_world2)
                ret.append(new_world2)
                metas.append(meta2)
            else:
                new_world1.push_box(1)
                meta1 = self.meta_conseguida(new_world1)
                ret.append(new_world1)
                metas.append(meta1)
                new_world2.push_box(2)
                meta2 = self.meta_conseguida(new_world2)
                ret.append(new_world2)
                metas.append(meta2)
            return ret, metas

        # En este estado el mono ha empujado la caja y ahora debe moverse a esa misma posicion
        if not self.bananas_picked and self.box_pos is self.banana_pos and self.box_pos is not self.monkey_pos:
            if self.monkey_pos == 1:
                new_world1.move_monkey(2)
                meta1 = self.meta_conseguida(new_world1)
                ret.append(new_world1)
                metas.append(meta1)
                new_world2.move_monkey(3)
                meta2 = self.meta_conseguida(new_world2)
                ret.append(new_world2)
                metas.append(meta2)
            elif self.monkey_pos == 2:
                new_world1.move_monkey(1)
                meta1 = self.meta_conseguida(new_world1)
                ret.append(new_world1)
                metas.append(meta1)
                new_world2.move_monkey(3)
                meta2 = self.meta_conseguida(new_world2)
                ret.append(new_world2)
                metas.append(meta2)
            else:
                new_world1.move_monkey(1)
                meta1 = self.meta_conseguida(new_world1)
                ret.append(new_world1)
                metas.append(meta1)
                new_world2.move_monkey(2)
                meta2 = self.meta_conseguida(new_world2)
                ret.append(new_world2)
                metas.append(meta2)
            return ret, metas

        # El mono y la caja estan en la misma posicion que las bananas, y el mono debe subirse a la caja para cogerlas
        if not self.bananas_picked and self.monkey_pos is self.box_pos and self.banana_pos is self.box_pos and not self.is_monkey_on_box:
            new_world1.climb_box()
            meta1 = self.meta_conseguida(new_world1)
            ret.append(new_world1)
            metas.append(meta1)
            return ret, metas

        # El mono ya se ha subido a la caja para recoger las bananas
        if not self.bananas_picked and self.monkey_pos is self.box_pos and self.banana_pos is self.box_pos and self.is_monkey_on_box:
            new_world1.pick_bananas()
            meta1 = self.meta_conseguida(new_world1)
            ret.append(new_world1)
            metas.append(meta1)
            return ret, metas

    # Diferentes metas que se deben satisfacer para conseguir el objetivo
    def meta_conseguida(self, world_state):
        # Meta 1: Moverse a la misma posicion que la caja
        if world_state.monkey_pos is world_state.box_pos and world_state.box_pos is not world_state.banana_pos:
            return 1
        # Meta 2: Empujar la caja a la misma posicion que los platanos
        if world_state.box_pos is world_state.banana_pos and world_state.monkey_pos is not world_state.box_pos:
            return 2
        # Meta 3: Moverse a la misma posicion que la caja y los platanos
        if world_state.monkey_pos is world_state.box_pos and world_state.box_pos is world_state.banana_pos and not world_state.is_monkey_on_box:
            return 3
        # Meta 4: Subirse encima de la caja
        if not world_state.bananas_picked and world_state.monkey_pos is world_state.box_pos and world_state.box_pos is world_state.banana_pos and world_state.is_monkey_on_box:
            return 4
        # Meta 5: Coger los platanos
        if world_state.bananas_picked:
            return 5
        return 0

    # Esta funcion es donde se implementa la planificacion basada en STRIPS
    def strips(self, world):
        new_world = world
        new_world.print_state()
        print("")
        # Mientras que las metas no esten satisfechas
        while new_world.meta_conseguida(new_world) != 5:

            # calcular en que meta estamos ahora mismo
            meta = new_world.meta_conseguida(new_world)

            # crear una lista con cada estado posible partiendo del estado inicial
            moves, metas = new_world.generate_child(new_world)

            for i in range(len(moves)):
                print("++++++ Posible movimiento ++++++")
                moves[i].print_state()
                print("Meta en estado actual: " + str(meta))
                print("Meta haciendo este movimiento: " + str(metas[i]))
                print("++++++++++++++++++++++++++++++++")
                print("")

                # Comparar la meta de cada movimiento posible en el estado actual
                # Si es mas grande que la meta actual, hacer el movimiento
                if metas[i] > meta:
                    new_world = moves[i]

            new_world.print_state()
            print("")

        print("")
        print("Los platanos han sido recogidos!")



def main():
    monkey_position = int(input("Poner la posicion del mono: "))
    bananas_position = int(input("Poner la posicion de las bananas: "))
    box_position = int(input("Poner la posicion de la caja: "))
    my_world = World(monkey_position, bananas_position, box_position)
    my_world.strips(my_world)

if __name__ == "__main__":
    main()



