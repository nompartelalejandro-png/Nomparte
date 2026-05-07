mkdir -p src/app/api/albaranes \
src/app/albaranes \
src/components \
src/lib \
src/types \
public/uploads && \

cat > src/types/albaran.ts << 'EOF'
export interface Albaran {
  id: string;
  numero: string;
  fecha: string;
  trabajador: string;
  partidaPresupuesto: string;
  gastos: number;
  comentarios: string;
  fotos?: string[];
}
EOF

cat > src/components/AlbaranForm.tsx << 'EOF'
"use client";

import { useState } from "react";

export default function AlbaranForm() {
  const [form, setForm] = useState({
    numero: "",
    fecha: "",
    trabajador: "",
    partidaPresupuesto: "",
    gastos: "",
    comentarios: "",
  });

  const [fotos, setFotos] = useState<FileList | null>(null);

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();

    const data = new FormData();

    Object.entries(form).forEach(([key, value]) => {
      data.append(key, value);
    });

    if (fotos) {
      Array.from(fotos).forEach((foto) => {
        data.append("fotos", foto);
      });
    }

    const res = await fetch("/api/albaranes", {
      method: "POST",
      body: data,
    });

    if (res.ok) {
      alert("Albarán guardado");
    }
  };

  return (
    <form
      onSubmit={handleSubmit}
      className="max-w-2xl mx-auto p-6 space-y-4 bg-white rounded-xl shadow"
    >
      <h1 className="text-2xl font-bold">Nuevo Albarán</h1>

      <input
        className="w-full border p-2 rounded"
        placeholder="Número de albarán"
        onChange={(e) => setForm({ ...form, numero: e.target.value })}
      />

      <input
        type="date"
        className="w-full border p-2 rounded"
        onChange={(e) => setForm({ ...form, fecha: e.target.value })}
      />

      <input
        className="w-full border p-2 rounded"
        placeholder="Trabajador"
        onChange={(e) => setForm({ ...form, trabajador: e.target.value })}
      />

      <input
        className="w-full border p-2 rounded"
        placeholder="Partida del presupuesto"
        onChange={(e) =>
          setForm({ ...form, partidaPresupuesto: e.target.value })
        }
      />

      <input
        type="number"
        className="w-full border p-2 rounded"
        placeholder="Gastos"
        onChange={(e) => setForm({ ...form, gastos: e.target.value })}
      />

      <textarea
        className="w-full border p-2 rounded"
        placeholder="Comentarios"
        onChange={(e) => setForm({ ...form, comentarios: e.target.value })}
      />

      <input
        type="file"
        multiple
        accept="image/*"
        onChange={(e) => setFotos(e.target.files)}
      />

      <button
        type="submit"
        className="bg-blue-600 text-white px-4 py-2 rounded"
      >
        Guardar
      </button>
    </form>
  );
}
EOF

cat > src/app/albaranes/page.tsx << 'EOF'
import AlbaranForm from "@/components/AlbaranForm";

export default function Page() {
  return (
    <main className="min-h-screen bg-gray-100 p-8">
      <AlbaranForm />
    </main>
  );
}
EOF

cat > src/app/api/albaranes/route.ts << 'EOF'
import { NextRequest, NextResponse } from "next/server";
import fs from "fs";
import path from "path";

export async function POST(req: NextRequest) {
  const data = await req.formData();

  const numero = data.get("numero");
  const fecha = data.get("fecha");
  const trabajador = data.get("trabajador");
  const partidaPresupuesto = data.get("partidaPresupuesto");
  const gastos = data.get("gastos");
  const comentarios = data.get("comentarios");

  const fotos = data.getAll("fotos") as File[];

  const fotosGuardadas: string[] = [];

  for (const foto of fotos) {
    if (!foto.name) continue;

    const bytes = await foto.arrayBuffer();
    const buffer = Buffer.from(bytes);

    const filePath = path.join(
      process.cwd(),
      "public/uploads",
      foto.name
    );

    fs.writeFileSync(filePath, buffer);

    fotosGuardadas.push("/uploads/" + foto.name);
  }

  console.log({
    numero,
    fecha,
    trabajador,
    partidaPresupuesto,
    gastos,
    comentarios,
    fotosGuardadas,
  });

  return NextResponse.json({
    ok: true,
  });
}
EOF
