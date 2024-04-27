SELECT
    COUNT(DISTINCT id) AS Acidentes_Problemas_Pista
FROM acidentes_rodovias_prf
WHERE causa_acidente IN ('Iluminação deficiente', 'Animais na Pista', 'Objeto estático sobre o leito carroçável', 'Falta de elemento de contenção que evite a saída do leito carroçável', 'Sinalização mal posicionada', 'Curva acentuada', 'Pista em desnível', 'Acumulo de água sobre o pavimento', 'Pista esburacada', 'Afundamento ou ondulação no pavimento', 'Demais falhas na via', 'Acumulo de areia ou detritos sobre o pavimento', 'Deficiência do Sistema de Iluminação/Sinalização', 'Falta de acostamento', 'Ausência de sinalização', 'Obstrução na via', 'Área urbana sem a presença de local apropriado para a travessia de pedestres', 'Restrição de visibilidade em curvas horizontais', 'Demais Fenômenos da natureza', 'Restrição de visibilidade em curvas verticais', 'Sinalização encoberta', 'Faixas de trânsito com largura insuficiente', 'Semáforo com defeito');

SELECT
    COUNT(DISTINCT id) AS Acidentes_Problemas_Pista
FROM acidentes_rodovias_prf
WHERE causa_acidente IN ('Iluminação deficiente', 'Animais na Pista', 'Objeto estático sobre o leito carroçável', 'Falta de elemento de contenção que evite a saída do leito carroçável', 'Sinalização mal posicionada', 'Curva acentuada', 'Pista em desnível', 'Acumulo de água sobre o pavimento', 'Pista esburacada', 'Afundamento ou ondulação no pavimento', 'Demais falhas na via', 'Acumulo de areia ou detritos sobre o pavimento', 'Deficiência do Sistema de Iluminação/Sinalização', 'Falta de acostamento', 'Ausência de sinalização', 'Obstrução na via', 'Área urbana sem a presença de local apropriado para a travessia de pedestres', 'Restrição de visibilidade em curvas horizontais', 'Demais Fenômenos da natureza', 'Restrição de visibilidade em curvas verticais', 'Sinalização encoberta', 'Faixas de trânsito com largura insuficiente', 'Semáforo com defeito')
AND mortos >=1;

SELECT
    regiao AS Regiao,
    COUNT(DISTINCT id) AS Acidentes_Problemas_Pista
FROM acidentes_rodovias_prf
WHERE causa_acidente IN (
    'Iluminação deficiente', 'Animais na Pista', 
    'Objeto estático sobre o leito carroçável', 
    'Falta de elemento de contenção que evite a saída do leito carroçável', 
    'Sinalização mal posicionada', 'Curva acentuada', 'Pista em desnível', 
    'Acumulo de água sobre o pavimento', 'Pista esburacada', 
    'Afundamento ou ondulação no pavimento', 'Demais falhas na via', 
    'Acumulo de areia ou detritos sobre o pavimento', 
    'Deficiência do Sistema de Iluminação/Sinalização', 
    'Falta de acostamento', 'Ausência de sinalização', 
    'Obstrução na via', 
    'Área urbana sem a presença de local apropriado para a travessia de pedestres', 
    'Restrição de visibilidade em curvas horizontais', 
    'Demais Fenômenos da natureza', 
    'Restrição de visibilidade em curvas verticais', 
    'Sinalização encoberta', 'Faixas de trânsito com largura insuficiente', 
    'Semáforo com defeito')
GROUP BY regiao
ORDER BY Acidentes_Problemas_Pista DESC;

SELECT
    regiao AS Regiao,
    COUNT(DISTINCT id) AS Acidentes_Problemas_Pista
FROM acidentes_rodovias_prf
WHERE causa_acidente IN (
    'Iluminação deficiente', 'Animais na Pista', 
    'Objeto estático sobre o leito carroçável', 
    'Falta de elemento de contenção que evite a saída do leito carroçável', 
    'Sinalização mal posicionada', 'Curva acentuada', 'Pista em desnível', 
    'Acumulo de água sobre o pavimento', 'Pista esburacada', 
    'Afundamento ou ondulação no pavimento', 'Demais falhas na via', 
    'Acumulo de areia ou detritos sobre o pavimento', 
    'Deficiência do Sistema de Iluminação/Sinalização', 
    'Falta de acostamento', 'Ausência de sinalização', 
    'Obstrução na via', 
    'Área urbana sem a presença de local apropriado para a travessia de pedestres', 
    'Restrição de visibilidade em curvas horizontais', 
    'Demais Fenômenos da natureza', 
    'Restrição de visibilidade em curvas verticais', 
    'Sinalização encoberta', 'Faixas de trânsito com largura insuficiente', 
    'Semáforo com defeito')
    AND mortos >= 1
GROUP BY regiao
ORDER BY Acidentes_Problemas_Pista DESC;
