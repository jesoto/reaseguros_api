🔍 Realizar una comparación **ítem por ítem**, asegurando que se comparen los **31 ítems completos** entre la póliza y cada slip de reaseguro.

📊 Genera un cuadro comparativo en formato JSON con la siguiente estructura:

- "N": número del ítem (del 1 al 31, sin omisiones ni saltos).
- "SECCIÓN_PÓLIZA": sección de la póliza donde aparece el ítem.
- "ITEM_PÓLIZA": nombre del ítem.
- "DETALLE_ÍTEM (Póliza)": contenido del ítem en la póliza.
- Por cada slip de reaseguro:
    [Nombre del Reasegurador N]: el nombre exacto que figura en el documento PDF.
   - "DETALLE - [Nombre del Reasegurador N] (Slip)": contenido del ítem en el slip.
   - "COMPARACIÓN [Nombre del Reasegurador N] (Slip)": comparación entre póliza y slip, usando los siguientes íconos:
     - ✅ Coincidencia
     - ⚠️ Inconsistencia menor
     - ❌ Discrepancia crítica

- "CONCLUSIÓN GENERAL": evaluación final del ítem comparado entre póliza y todos los slips.

⚠️ IMPORTANTE:
- Asegúrate de que se generen **exactamente 31 ítems** en el resultado.
- Si algún slip no tiene el ítem, indica "No presente" y marca como ❌.
- No omitas ningún número ni ítem, aunque no haya información en el slip.

Formato de salida: JSON estructurado para 31 ítems completos.

## **SECCIONES Y ITEMS**
## DATOS GENERALES
- **TIPO**
- **ASEGURADOS**
- **MONEDA**
- **VIGENCIA**
- **ACTIVIDAD O GIRO DEL NEGOCIO**
- **RELACION DE LOCALES ASEGURADOS**

## CONDICIONES
- **GARANTIAS**
- **RECOMENDACIÓN**
- **CONDICIONES ESPECIALES**
- **SUBJETIVIDADES**
- **EXCLUSIONES**: 

## ESPECIFICACIONES DEL SEGURO

- **MATERIA DEL SEGURO**
- **ESQUEMA ASEGURATIVO**
- **BASES DE AVALUO E INDEMNIZACIÓN**
- **BIENES ASEGURADOS Y VALORES DECLARADOS**
- **MODALIDAD DE ASEGURAMIENTO**
- **COBERTURAS**

## FINANCIERO
- **TASA**
- **PRIMA NETA**

## ESTRUCTURA
- **COASEGURO**

## SUMAS Y LIMITES
- **SUMAS ASEGURADAS**
- **SUB LIMITES**
- **DEDUCIBLE/EXCESO**

## LEGAL Y JURISDICCION
- **CONDICIONES**
- **LIMITES TERRITORIALES**
- **LEY Y JURISDICCION**

## OTROS
- **ANOMALIAS/TACHADURAS**
- **SELLOS Y PARTICIPACION**

## RIESGOS CRITICOS
- **CLAUSULA ESPECIAL - FRONTING**
- **CLAUSULA DE COOPERACION DE RECLAMOS**
- **PROPORCION DE SEGUROS**

---

