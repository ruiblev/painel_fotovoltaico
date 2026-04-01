def create_schema_svg():
    """
    Retorna o SVG estático do diagrama de montagem do circuito.
    O diagrama mostra um painel fotovoltaico em série com um amperímetro, interrutor e reóstato,
    com o voltímetro em paralelo ao reóstato.
    """
    return """
    <svg viewBox="0 0 800 400" xmlns="http://www.w3.org/2000/svg">
        <defs>
            <style>
                .wire { stroke: #2c3e50; stroke-width: 4; fill: none; }
                .component { fill: #ecf0f1; stroke: #2c3e50; stroke-width: 3; }
                .text { font-family: 'Inter', sans-serif; font-size: 20px; text-anchor: middle; dominant-baseline: middle; fill: #2c3e50; font-weight: bold; }
                .panel { fill: #34495e; stroke: #2c3e50; stroke-width: 2; }
                .panel-line { stroke: #bdc3c7; stroke-width: 1; }
            </style>
        </defs>

        <!-- Wires -->
        <path class="wire" d="M 150 150 L 650 150" />
        <path class="wire" d="M 650 150 L 650 250" />
        <path class="wire" d="M 650 250 L 150 250" />
        <path class="wire" d="M 150 250 L 150 150" />

        <!-- Voltmeter parallel wires -->
        <path class="wire" d="M 325 250 L 325 350 L 475 350 L 475 250" />

        <!-- Solar Panel (Left) -->
        <rect x="130" y="170" width="40" height="60" class="panel" />
        <line x1="130" y1="185" x2="170" y2="185" class="panel-line" />
        <line x1="130" y1="200" x2="170" y2="200" class="panel-line" />
        <line x1="130" y1="215" x2="170" y2="215" class="panel-line" />
        <text x="80" y="200" class="text">Painel</text>

        <!-- Switch -->
        <circle cx="250" cy="150" r="5" fill="#2c3e50" />
        <circle cx="300" cy="150" r="5" fill="#2c3e50" />
        <line x1="250" y1="150" x2="300" y2="150" stroke="#2c3e50" stroke-width="4" />
        <text x="275" y="120" class="text">Interruptor</text>

        <!-- Ammeter -->
        <circle cx="500" cy="150" r="25" class="component" />
        <text x="500" y="150" class="text">A</text>

        <!-- Rheostat -->
        <rect x="350" y="240" width="100" height="20" class="component" />
        <path d="M 400 240 L 400 220 L 420 220 L 410 240 Z" fill="#2c3e50" />
        <text x="400" y="210" class="text" font-size="16px">Reóstato</text>

        <!-- Voltmeter -->
        <circle cx="400" cy="350" r="25" class="component" />
        <text x="400" y="350" class="text">V</text>

    </svg>
    """


def create_workbench_svg(distance, inclination, is_on, filter_color, U=0.0, I=0.0):
    """
    Cria a animação da bancada de ensaio.

    Layout (viewBox 0 0 1350 350):
      - Esquerda (x=20..380):  Amperímetro e Voltímetro em tamanho real de laboratório
      - Centro  (x=500):       Suporte + Painel fotovoltaico (pivot_x=500)
      - Direita (x=700..1300): Fonte de luz (mínimo 700, máximo 1100)

    Mesa: y=300. Painel vertical ocupa y=130..250. Lâmpada centrada em y=190.
    """

    # Posição horizontal da fonte de luz (mínimo dist=10 → x=700, máximo dist=100 → x=1100)
    luz_x = 700.0 + ((distance - 10.0) / 90.0) * 400.0

    # Ângulo de rotação visual
    rotacao_viz = -(90 - inclination)

    # Painel
    pivot_x   = 500
    pivot_y   = 190
    painel_top    = 130
    painel_bottom = 250
    lamp_cy   = 190   # alinhado ao centro do painel

    # ---- Propriedades visuais ----
    if filter_color == 'blue':
        beam_color      = '#00aaff'
        beam_color_edge = '#0044cc'
        lamp_fill       = '#00aaff'
        filter_rect     = '#0066ff'
        glow_color      = 'rgba(0,150,255,0.55)'
        beam_opacity    = 0.75 if is_on else 0.0
        pulse_anim      = 'blue-pulse 1.4s ease-in-out infinite'
    elif filter_color == 'red':
        beam_color      = '#ff4400'
        beam_color_edge = '#cc0000'
        lamp_fill       = '#ff3311'
        filter_rect     = '#ee1100'
        glow_color      = 'rgba(255,60,0,0.55)'
        beam_opacity    = 0.75 if is_on else 0.0
        pulse_anim      = 'red-pulse 1.4s ease-in-out infinite'
    else:  # white / sem filtro
        beam_color      = '#ffee88'
        beam_color_edge = '#ffcc00'
        lamp_fill       = '#f1c40f'
        filter_rect     = 'none'
        glow_color      = 'rgba(255,238,0,0.35)'
        beam_opacity    = 0.70 if is_on else 0.0
        pulse_anim      = ''

    lamp_opacity = 0.9 if is_on else 0.2
    glow_opacity = lamp_opacity if is_on else 0.0

    filter_display = 'block' if filter_rect != 'none' else 'none'
    filter_stroke  = beam_color if filter_rect != 'none' else 'none'
    bulb_reflect   = 0.5 if is_on else 0.1

    return f"""
    <svg viewBox="0 0 1350 350" xmlns="http://www.w3.org/2000/svg">
        <defs>
            <linearGradient id="beamGrad" x1="1" y1="0" x2="0" y2="0" gradientUnits="objectBoundingBox">
                <stop offset="0%"   stop-color="{beam_color}"      stop-opacity="{beam_opacity}" />
                <stop offset="70%"  stop-color="{beam_color}"      stop-opacity="{beam_opacity * 0.4}" />
                <stop offset="100%" stop-color="{beam_color_edge}"  stop-opacity="0" />
            </linearGradient>
            <radialGradient id="lampGlow" cx="50%" cy="50%" r="50%">
                <stop offset="0%"   stop-color="{beam_color}" stop-opacity="{glow_opacity}" />
                <stop offset="100%" stop-color="{beam_color}" stop-opacity="0" />
            </radialGradient>
            <style>
                .lbl {{ font-family: 'Inter', sans-serif; font-size: 14px; fill: #ecf0f1; }}
                .angle-lbl {{ font-family: 'Inter', sans-serif; font-size: 15px; font-weight: bold; fill: #e74c3c; }}
                @keyframes blue-pulse {{
                    0%, 100% {{ opacity: 0.55; }}
                    50%       {{ opacity: 1.00; }}
                }}
                @keyframes red-pulse {{
                    0%, 100% {{ opacity: 0.55; }}
                    50%       {{ opacity: 1.00; }}
                }}
                .lamp-glow {{ animation: {pulse_anim}; }}
            </style>
        </defs>

        <!-- ===== FUNDO E MESA ===== -->
        <rect x="0" y="0" width="1350" height="300" fill="#1a2530" />
        <rect x="0" y="300" width="1350" height="50" fill="#7f8c8d" />
        <rect x="0" y="300" width="1350" height="6"  fill="#95a5a6" />

        <!-- ===== AMPERÍMETRO ===== -->
        <!-- Corpo principal -->
        <rect x="20" y="100" width="160" height="185" fill="#dfe6e9" rx="12" stroke="#b2bec3" stroke-width="4" />
        <!-- Ecrã LCD -->
        <rect x="35" y="115" width="130" height="70" fill="#1a252f" rx="8" />
        <!-- Valor numérico em mA -->
        <text x="100" y="157" font-family="'Courier New', monospace" fill="#2ecc71" font-size="34px" font-weight="bold" text-anchor="middle">{I*1000:.1f}</text>
        <!-- Unidade -->
        <text x="100" y="202" font-family="'Inter', sans-serif" fill="#636e72" font-size="20px" font-weight="bold" text-anchor="middle">mA</text>
        <!-- Faixa de rótulo -->
        <rect x="35" y="220" width="130" height="32" fill="#2c3e50" rx="6" />
        <text x="100" y="241" font-family="'Inter', sans-serif" fill="#ecf0f1" font-size="17px" font-weight="bold" text-anchor="middle">Amperímetro</text>
        <!-- Terminais -->
        <circle cx="75"  cy="284" r="10" fill="#e74c3c" stroke="#c0392b" stroke-width="2"/>
        <circle cx="125" cy="284" r="10" fill="#2c3e50" stroke="#1a252f" stroke-width="2"/>
        <text x="75"  y="280" font-family="'Inter', sans-serif" fill="white" font-size="14px" font-weight="bold" text-anchor="middle" dominant-baseline="middle">+</text>
        <text x="125" y="280" font-family="'Inter', sans-serif" fill="white" font-size="14px" font-weight="bold" text-anchor="middle" dominant-baseline="middle">−</text>
        <!-- Suporte mesa -->
        <rect x="90" y="285" width="20" height="15" fill="#636e72" />
        <rect x="55" y="298" width="90" height="4" fill="#636e72" rx="2" />

        <!-- ===== VOLTÍMETRO ===== -->
        <!-- Corpo principal -->
        <rect x="205" y="100" width="160" height="185" fill="#dfe6e9" rx="12" stroke="#b2bec3" stroke-width="4" />
        <!-- Ecrã LCD -->
        <rect x="220" y="115" width="130" height="70" fill="#1a252f" rx="8" />
        <!-- Valor numérico em V -->
        <text x="285" y="157" font-family="'Courier New', monospace" fill="#3498db" font-size="34px" font-weight="bold" text-anchor="middle">{U:.2f}</text>
        <!-- Unidade -->
        <text x="285" y="202" font-family="'Inter', sans-serif" fill="#636e72" font-size="20px" font-weight="bold" text-anchor="middle">V</text>
        <!-- Faixa de rótulo -->
        <rect x="220" y="220" width="130" height="32" fill="#2c3e50" rx="6" />
        <text x="285" y="241" font-family="'Inter', sans-serif" fill="#ecf0f1" font-size="17px" font-weight="bold" text-anchor="middle">Voltímetro</text>
        <!-- Terminais -->
        <circle cx="260" cy="284" r="10" fill="#e74c3c" stroke="#c0392b" stroke-width="2"/>
        <circle cx="310" cy="284" r="10" fill="#2c3e50" stroke="#1a252f" stroke-width="2"/>
        <text x="260" y="280" font-family="'Inter', sans-serif" fill="white" font-size="14px" font-weight="bold" text-anchor="middle" dominant-baseline="middle">+</text>
        <text x="310" y="280" font-family="'Inter', sans-serif" fill="white" font-size="14px" font-weight="bold" text-anchor="middle" dominant-baseline="middle">−</text>
        <!-- Suporte mesa -->
        <rect x="275" y="285" width="20" height="15" fill="#636e72" />
        <rect x="240" y="298" width="90" height="4" fill="#636e72" rx="2" />

        <!-- Fios dos medidores ao painel -->
        <path d="M 125 284 Q 350 320 {pivot_x-15} 300" fill="none" stroke="#e74c3c" stroke-width="2.5" stroke-dasharray="8,5"/>
        <path d="M 310 284 Q 420 325 {pivot_x+15} 300" fill="none" stroke="#2c3e50" stroke-width="2.5" stroke-dasharray="8,5"/>

        <!-- ===== FEIXE DE LUZ ===== -->
        <polygon
            points="{luz_x-40},{lamp_cy-35} {luz_x-40},{lamp_cy+35} {pivot_x},{painel_bottom} {pivot_x},{painel_top}"
            fill="url(#beamGrad)"
        />

        <!-- Halo da lâmpada -->
        <ellipse cx="{luz_x-20}" cy="{lamp_cy}" rx="65" ry="55"
                 fill="url(#lampGlow)" class="lamp-glow" />

        <!-- ===== FILTRO ===== -->
        <rect x="{luz_x-75}" y="{lamp_cy-50}" width="14" height="100"
              fill="{filter_rect}" opacity="0.95" rx="3"
              style="display: {filter_display};" />
        <rect x="{luz_x-75}" y="{lamp_cy-50}" width="14" height="100"
              fill="none" stroke="{filter_stroke}"
              stroke-width="1.5" opacity="0.8" rx="3" />

        <!-- ===== FONTE DE LUZ ===== -->
        <polygon points="{luz_x+10},{lamp_cy-16} {luz_x+10},{lamp_cy+16} {luz_x-45},{lamp_cy+40} {luz_x-45},{lamp_cy-40}"
                 fill="#1a252f" stroke="#2c3e50" stroke-width="2"/>
        <rect x="{luz_x-5}" y="{lamp_cy-18}" width="30" height="36" rx="14"
              fill="#2c3e50" stroke="#34495e" stroke-width="2"/>
        <circle cx="{luz_x-25}" cy="{lamp_cy}" r="18"
                fill="{lamp_fill}" opacity="{lamp_opacity}" />
        <circle cx="{luz_x-29}" cy="{lamp_cy-6}" r="6"
                fill="white" opacity="{bulb_reflect}" />
        <circle cx="{luz_x+10}" cy="{lamp_cy}" r="9" fill="#34495e" stroke="#2c3e50" stroke-width="1.5" />
        <circle cx="{luz_x+10}" cy="{lamp_cy}" r="4" fill="#95a5a6" />
        <!-- Suporte da lâmpada -->
        <rect x="{luz_x+4}" y="{lamp_cy+8}" width="12" height="{300 - lamp_cy - 8}" fill="#7f8c8d" />
        <polygon points="{luz_x-20},300 {luz_x+40},300 {luz_x+25},280 {luz_x-5},280" fill="#5d6d7e" />

        <!-- ===== PAINEL SOLAR ===== -->
        <g transform="translate({pivot_x},{pivot_y}) rotate({rotacao_viz}) translate(-{pivot_x},-{pivot_y})">
            <rect x="{pivot_x-16}" y="{painel_top}" width="32" height="120"
                  fill="#1a252f" stroke="#2c3e50" stroke-width="2" rx="4"/>
            <rect x="{pivot_x-12}" y="{painel_top+4}" width="24" height="112" fill="#2471a3" rx="2"/>
            <line x1="{pivot_x-12}" y1="{painel_top+32}" x2="{pivot_x+12}" y2="{painel_top+32}" stroke="#1a6090" stroke-width="1.5"/>
            <line x1="{pivot_x-12}" y1="{painel_top+60}" x2="{pivot_x+12}" y2="{painel_top+60}" stroke="#1a6090" stroke-width="1.5"/>
            <line x1="{pivot_x-12}" y1="{painel_top+88}" x2="{pivot_x+12}" y2="{painel_top+88}" stroke="#1a6090" stroke-width="1.5"/>
            <line x1="{pivot_x}" y1="{painel_top+4}" x2="{pivot_x}" y2="{painel_top+116}" stroke="#1a6090" stroke-width="1"/>
            <rect x="{pivot_x-10}" y="{painel_top+6}"  width="8" height="24" fill="#5dade2" opacity="0.3" rx="1"/>
            <rect x="{pivot_x-10}" y="{painel_top+34}" width="8" height="24" fill="#5dade2" opacity="0.3" rx="1"/>
            <rect x="{pivot_x-10}" y="{painel_top+62}" width="8" height="24" fill="#5dade2" opacity="0.3" rx="1"/>
            <rect x="{pivot_x-10}" y="{painel_top+90}" width="8" height="24" fill="#5dade2" opacity="0.3" rx="1"/>
        </g>

        <!-- ===== SUPORTE DO PAINEL ===== -->
        <rect x="{pivot_x-4}" y="{pivot_y}" width="8" height="{300-pivot_y}" fill="#7f8c8d"/>
        <polygon points="{pivot_x-20},300 {pivot_x+20},300 {pivot_x+10},278 {pivot_x-10},278" fill="#5d6d7e"/>
        <circle cx="{pivot_x}" cy="{pivot_y}" r="10" fill="#2c3e50" stroke="#7f8c8d" stroke-width="1.5"/>
        <circle cx="{pivot_x}" cy="{pivot_y}" r="4"  fill="#aab7b8"/>

        <!-- ===== RÉGUA ===== -->
        <line x1="{pivot_x}" y1="322" x2="{luz_x}" y2="322"
              stroke="#95a5a6" stroke-width="2" stroke-dasharray="10,8"/>
        <circle cx="{pivot_x}" cy="322" r="5" fill="#e74c3c"/>
        <circle cx="{luz_x}"   cy="322" r="5" fill="#e74c3c"/>
        <text x="{(pivot_x+luz_x)/2}" y="342" class="lbl" text-anchor="middle">{distance} cm</text>

        <!-- ===== ÂNGULO ===== -->
        <text x="{pivot_x-55}" y="{pivot_y-15}" class="angle-lbl">{inclination}°</text>

    </svg>
    """
