import sys

class UniversalTuringMachine:
    def __init__(self, encoded_input: str):
        """
        Simulador de Máquina de Turing Universal (MTU).
        Formato de entrada: <EstadoInicial>*<CintaEntrada>$<Quintupla1>#<Quintupla2>#...
        El '*' se ubica justo antes del símbolo sobre el que inicia el cabezal.
        """
        self.raw_input = encoded_input.strip()
        self.transitions = {}
        self.tape = []
        self.head_pos = 0
        self.current_state = ""
        
        self._parse_encoding()

    def _parse_encoding(self):
        # 1. Separar la configuración inicial de la tabla de transiciones
        if '$' not in self.raw_input:
            raise ValueError("Formato inválido: Falta el separador '$'.")

        config_part, transitions_part = self.raw_input.split('$', 1)

        if '*' not in config_part:
            raise ValueError("Formato inválido: Falta el asterisco '*' en la configuración inicial.")

        # 2. Parsear la tabla de transiciones (Quíntuplas)
        raw_quintuples = transitions_part.split('#')
        for q in raw_quintuples:
            if not q:
                continue
            
            # Formato de quíntupla de tamaño variable (por el '111'):
            curr_state = q[:3]
            rem = q[3:]
            
            # Símbolo leído ('111' para blanco, '0' o '1' para bits)
            if rem.startswith("111"):
                read_sym = "111"
                rem = rem[3:]
            else:
                read_sym = rem[0]
                rem = rem[1:]
                
            # Nuevo estado (3 bits)
            new_state = rem[:3]
            rem = rem[3:]
            
            # Símbolo escrito ('111' para blanco, '0' o '1' para bits)
            if rem.startswith("111"):
                write_sym = "111"
                rem = rem[3:]
            else:
                write_sym = rem[0]
                rem = rem[1:]
                
            # Movimiento: últimos 2 bits ('00'=R, '01'=L, '10'=S)
            mov = rem
            
            self.transitions[(curr_state, read_sym)] = (new_state, write_sym, mov)

        # 3. Parsear la cinta y el estado inicial
        state_part, tape_part = config_part.split('*', 1)
        self.current_state = state_part
        
        # La cinta es exactamente la secuencia que sigue al '*'
        self.tape = list(tape_part) if tape_part else ['111']
        self.head_pos = 0

    def print_tape_state(self, step: int):
        tape_str = ""
        for i, char in enumerate(self.tape):
            symbol_display = "□" if char == "111" else char
            if i == self.head_pos:
                tape_str += f"[{symbol_display}]"
            else:
                tape_str += f" {symbol_display} "
        print(f"Paso {step:02d} | Estado: {self.current_state} | Cinta: {tape_str}")

    def run(self, max_steps: int = 1000):
        print("=== SIMULACIÓN PASO A PASO DE LA MTU ===")
        step = 0
        
        while step < max_steps:
            # Expansión dinámica de la cinta
            if self.head_pos >= len(self.tape):
                self.tape.append('111')
            elif self.head_pos < 0:
                self.tape.insert(0, '111')
                self.head_pos = 0

            self.print_tape_state(step)

            # Estado final de aceptación (qacc = '110')
            if self.current_state == "110":
                final_tape = "".join(["□" if c == "111" else c for c in self.tape])
                print(f"\n✅ Aceptada en {step} pasos.")
                print(f"Cinta final: {final_tape}")
                return True

            current_symbol = self.tape[self.head_pos]
            key = (self.current_state, current_symbol)

            if key not in self.transitions:
                print(f"\n❌ Transición no definida para el par ({self.current_state}, {current_symbol}). Ejecución abortada.")
                return False

            new_state, write_symbol, movement = self.transitions[key]

            # Actualizar celda y estado
            self.tape[self.head_pos] = write_symbol
            self.current_state = new_state

            # Mover cabezal ('00': R, '01': L, '10': S)
            if movement == "00":
                self.head_pos += 1
            elif movement == "01":
                self.head_pos -= 1

            step += 1

        print("\n⚠️ Se superó el límite máximo de pasos (Posible bucle infinito).")
        return False


if __name__ == "__main__":
    if len(sys.argv) > 1:
        cadena = sys.argv[1]
    else:
        cadena = input("Ingresá la cadena codificada de la MTU:\n").strip()

    simulador = UniversalTuringMachine(cadena)
    simulador.run()