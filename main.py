import numpy as np
import skfuzzy as fuzz
from skfuzzy import control as ctrl
from flask import Flask, request, jsonify, render_template
from flask_cors import CORS

app = Flask(__name__)
CORS(app, resources={r"/*": {"origins": "*"}})

# Route untuk halaman utama
@app.route('/')
def index():
    return render_template('index.html')

# Route untuk test page
@app.route('/test')
def test():
    return render_template('minimal_test.html')

# Variabel input
durasi = ctrl.Antecedent(np.arange(0,13,1), 'durasi')
gangguan = ctrl.Antecedent(np.arange(0,11,1), 'gangguan')
konsistensi = ctrl.Antecedent(np.arange(0,11,1), 'konsistensi')
stres = ctrl.Antecedent(np.arange(0,11,1), 'stres')

# Variabel output
kualitas = ctrl.Consequent(np.arange(0,11,1), 'kualitas')

# Membership function durasi
durasi['pendek'] = fuzz.trimf(durasi.universe, [0, 0, 5])
durasi['cukup'] = fuzz.trimf(durasi.universe, [4, 7, 9])
durasi['panjang'] = fuzz.trimf(durasi.universe, [8, 12, 12])

# Membership function gangguan
gangguan['sering'] = fuzz.trimf(gangguan.universe, [7, 10, 10])
gangguan['sedang'] = fuzz.trimf(gangguan.universe, [3, 5, 7])
gangguan['jarang'] = fuzz.trimf(gangguan.universe, [0, 0, 3])

# Membership function konsistensi
konsistensi['buruk'] = fuzz.trimf(konsistensi.universe, [0, 0, 4])
konsistensi['sedang'] = fuzz.trimf(konsistensi.universe, [3, 5, 7])
konsistensi['baik'] = fuzz.trimf(konsistensi.universe, [6, 10, 10])

# Membership function stres
stres['tinggi'] = fuzz.trimf(stres.universe, [7, 10, 10])
stres['sedang'] = fuzz.trimf(stres.universe, [3, 5, 7])
stres['rendah'] = fuzz.trimf(stres.universe, [0, 0, 3])

# Membership function kualitas
kualitas['rendah'] = fuzz.trimf(kualitas.universe, [0, 0, 4])
kualitas['sedang'] = fuzz.trimf(kualitas.universe, [3, 5, 7])
kualitas['tinggi'] = fuzz.trimf(kualitas.universe, [6, 10, 10])

# Rules
rules = [
    ctrl.Rule(durasi['pendek'] & gangguan['sering'], kualitas['rendah']),
    ctrl.Rule(durasi['cukup'] & konsistensi['baik'] & stres['rendah'], kualitas['tinggi']),
    ctrl.Rule(durasi['panjang'] & gangguan['jarang'] & konsistensi['baik'], kualitas['tinggi']),
    ctrl.Rule(konsistensi['buruk'] | stres['tinggi'], kualitas['rendah']),
    ctrl.Rule(durasi['cukup'] & gangguan['sedang'] & stres['sedang'], kualitas['sedang'])
]

system = ctrl.ControlSystem(rules)
sim = ctrl.ControlSystemSimulation(system)

@app.route('/fuzzy', methods=['POST'])
def fuzzy_sleep():
    data = request.json
    sim.input['durasi'] = float(data['durasi'])
    sim.input['gangguan'] = float(data['gangguan'])
    sim.input['konsistensi'] = float(data['konsistensi'])
    sim.input['stres'] = float(data['stres'])
    sim.compute()

    score = sim.output['kualitas']
    if score < 4:
        kategori = "Buruk"
    elif score < 7:
        kategori = "Sedang"
    else:
        kategori = "Baik"

    return jsonify({"kualitas_tidur": score, "kategori": kategori})

# Vercel deployment handler
app.debug = False

if __name__ == '__main__':
    app.run(debug=True)

# Export for Vercel
def handler(request):
    return app(request.environ, lambda status, headers: None)