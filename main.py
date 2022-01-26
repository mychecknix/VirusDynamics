#!/usr/bin/env python
from dataclasses import dataclass
import numpy as np
import tkinter as tk
from tkinter import messagebox
import matplotlib.pyplot as plt
import matplotlib.animation as animation
from matplotlib import style
from scipy.integrate import odeint


# alle globalen Werte/Eingabeparameter
# TODO: Alle möglichen eingabewerte Ergänzen und beschreiben!!! z.B. Immunantwortwerte
@dataclass
class Data:
    """
    ∀ parameters > 0
    """
    # la: (λ lambda) fix provided uninfected cells rate
    la: float = 1.0 * 10 ** 5
    # m: mortality rate uninfected cells
    m: float = 0.1
    # b: (ignored) => b=0
    b: float = 0.0
    # r: infection contact rate
    r: float = 8.0 * 10 ** -8
    # k: virus production rate
    k: float = 100.0
    # nu: (ν nu) length of stay of viruses in system
    nu: float = 10.0
    # mu: (μ mu) mortality rate infected cells
    mu: float = 0.5
    # s: Abbaurate Virus
    s: float = 0.00001
    # a: Produktionsrate T-Killerzellen
    a: float = 0.00005
    # n: Sterberate T-Killerzellen
    n: float = 0.9
    # V_0: Startwert freie Virionen
    v_0: float = 1000
    # Z_0: Startwert gesunde Zellen
    z_0: float = 1000000
    # I_0: Startwert infizierte Zellen
    i_0: float = 100
    # P_0: Startwert T-Killerzellen
    p_0: float = 100
    # t: Zeit in Zeiteinheiten; beziehungsweise Generationen
    t: int = 300


# Klasse für die Grafische Oberfläche mit dem Modul Tkinter
class InputDataGUI:
    def __init__(self):
        self.font_h1 = ("Helvetica", 18)
        self.font_text = ("Helvetica", 13)
        # Tkinter Objekt
        self.root = tk.Tk()
        self.root.title("Dynamik von Viren")
        # TODO: Icon verursacht Fehler bei der Ausführbaren Datei; Fehler bei Einbindung
        # icon https://www.iconfinder.com/icons/6013011/bacteria_corona_coronavirus_covid_virus_icon
        # self.root.iconbitmap('virus.ico')
        self.root.geometry("1280x720")
        style.use('ggplot')
        # Tkinter Frame zur Anordnung von Elementen
        self.frame1 = tk.Frame(self.root)
        # Parameter
        self.label1 = tk.Label(self.frame1, text="Parameter:", font=self.font_h1)
        self.label1.grid(row=0, column=0, columnspan=6, padx=5, pady=(15, 5), sticky='w')
        # b
        self.label_b = tk.Label(self.frame1, text="Produktionsrate gesunde Zellen (b):", font=self.font_text)
        self.label_b.grid(row=1, column=0, padx=5, pady=5, sticky='w')
        self.input_b = tk.Entry(self.frame1, width=10, font=self.font_text)
        self.input_b.grid(row=1, column=1, padx=5, pady=5)
        self.input_b.insert(0, str(data.b))
        self.input_b.bind("<Return>", self.on_change)
        # k
        self.label_k = tk.Label(self.frame1, text="Produktionsrate infizierte Zellen (k):", font=self.font_text)
        self.label_k.grid(row=2, column=0, padx=5, pady=5, sticky='w')
        self.input_k = tk.Entry(self.frame1, width=10, font=self.font_text)
        self.input_k.grid(row=2, column=1, padx=5, pady=5)
        self.input_k.insert(0, str(data.k))
        self.input_k.bind("<Return>", self.on_change)
        # lambda
        self.label_la = tk.Label(self.frame1, text="verfügbare gesunde Zellen (λ):", font=self.font_text)
        self.label_la.grid(row=3, column=0, padx=5, pady=5, sticky='w')
        self.input_la = tk.Entry(self.frame1, width=10, font=self.font_text)
        self.input_la.grid(row=3, column=1, padx=5, pady=5)
        self.input_la.insert(0, str(data.la))
        self.input_la.bind("<Return>", self.on_change)
        # m
        self.label_m = tk.Label(self.frame1, text="Sterberate gesunder Zellen (m):", font=self.font_text)
        self.label_m.grid(row=1, column=2, padx=(55, 5), pady=5, sticky='w')
        self.input_m = tk.Entry(self.frame1, width=10, font=self.font_text)
        self.input_m.grid(row=1, column=3, padx=5, pady=5)
        self.input_m.insert(0, str(data.m))
        self.input_m.bind("<Return>", self.on_change)
        # mu
        self.label_mu = tk.Label(self.frame1, text="Sterberate infizierter Zellen (μ):", font=self.font_text)
        self.label_mu.grid(row=2, column=2, padx=(55, 5), pady=5, sticky='w')
        self.input_mu = tk.Entry(self.frame1, width=10, font=self.font_text)
        self.input_mu.grid(row=2, column=3, padx=5, pady=5)
        self.input_mu.insert(0, str(data.mu))
        self.input_mu.bind("<Return>", self.on_change)
        # nu
        self.label_nu = tk.Label(self.frame1, text="Lebensdauer Virus (ν):", font=self.font_text)
        self.label_nu.grid(row=1, column=4, padx=(55, 5), pady=5, sticky='w')
        self.input_nu = tk.Entry(self.frame1, width=10, font=self.font_text)
        self.input_nu.grid(row=1, column=5, padx=5, pady=5)
        self.input_nu.insert(0, str(data.nu))
        self.input_nu.bind("<Return>", self.on_change)
        # r
        self.label_r = tk.Label(self.frame1, text="Infektionskontaktrate (r):", font=self.font_text)
        self.label_r.grid(row=2, column=4, padx=(55, 5), pady=5, sticky='w')
        self.input_r = tk.Entry(self.frame1, width=10, font=self.font_text)
        self.input_r.grid(row=2, column=5, padx=5, pady=5)
        self.input_r.insert(0, str(data.r))
        self.input_r.bind("<Return>", self.on_change)
        # Startwerte
        self.label1 = tk.Label(self.frame1, text="Startwerte:", font=self.font_h1)
        self.label1.grid(row=4, column=0, columnspan=6, padx=5, pady=(15, 5), sticky='w')
        # V_0
        self.label_v0 = tk.Label(self.frame1, text="freie Virionen zu Beginn (V_0):", font=self.font_text)
        self.label_v0.grid(row=5, column=0, padx=5, pady=5, sticky='w')
        self.input_v0 = tk.Entry(self.frame1, width=10, font=self.font_text)
        self.input_v0.grid(row=5, column=1, padx=5, pady=5)
        self.input_v0.insert(0, str(data.v_0))
        self.input_v0.bind("<Return>", self.on_change)
        # Z_0
        self.label_z0 = tk.Label(self.frame1, text="gesunde Zellen zu Beginn (Z_0):", font=self.font_text)
        self.label_z0.grid(row=5, column=2, padx=(55, 5), pady=5, sticky='w')
        self.input_z0 = tk.Entry(self.frame1, width=10, font=self.font_text)
        self.input_z0.grid(row=5, column=3, padx=5, pady=5)
        self.input_z0.insert(0, str(data.z_0))
        self.input_z0.bind("<Return>", self.on_change)
        # I_0
        self.label_i0 = tk.Label(self.frame1, text="infizierte Zellen zu Beginn (I_0):", font=self.font_text)
        self.label_i0.grid(row=5, column=4, padx=(55, 5), pady=5, sticky='w')
        self.input_i0 = tk.Entry(self.frame1, width=10, font=self.font_text)
        self.input_i0.grid(row=5, column=5, padx=5, pady=5)
        self.input_i0.insert(0, str(data.i_0))
        self.input_i0.bind("<Return>", self.on_change)
        # Zeit
        self.label1 = tk.Label(self.frame1, text="Generationen:", font=self.font_h1)
        self.label1.grid(row=6, column=0, columnspan=6, padx=5, pady=(15, 5), sticky='w')
        # t
        self.label_t = tk.Label(self.frame1, text="Zeit max (t):", font=self.font_text)
        self.label_t.grid(row=7, column=0, padx=5, pady=5, sticky='w')
        self.input_t = tk.Entry(self.frame1, width=10, font=self.font_text)
        self.input_t.grid(row=7, column=1, padx=5, pady=5)
        self.input_t.insert(0, str(data.t))
        self.input_t.bind("<Return>", self.on_change)
        # Immunantwort
        self.label1 = tk.Label(self.frame1, text="Immunantwort:", font=self.font_h1)
        self.label1.grid(row=8, column=0, columnspan=6, padx=5, pady=(15, 5), sticky='w')
        # P_0
        self.label_p0 = tk.Label(self.frame1, text="T-Killerzellen zu Beginn (P_0):", font=self.font_text)
        self.label_p0.grid(row=9, column=0, padx=5, pady=5, sticky='w')
        self.input_p0 = tk.Entry(self.frame1, width=10, font=self.font_text)
        self.input_p0.grid(row=9, column=1, padx=5, pady=5)
        self.input_p0.insert(0, str(data.p_0))
        self.input_p0.bind("<Return>", self.on_change)
        # a
        self.label_a = tk.Label(self.frame1, text="Produktionsrate T-Killerzellen (a):", font=self.font_text)
        self.label_a.grid(row=10, column=0, padx=5, pady=5, sticky='w')
        self.input_a = tk.Entry(self.frame1, width=10, font=self.font_text)
        self.input_a.grid(row=10, column=1, padx=5, pady=5)
        self.input_a.insert(0, str(data.a))
        self.input_a.bind("<Return>", self.on_change)
        # s
        self.label_s = tk.Label(self.frame1, text="Abbaurate Virus (s):", font=self.font_text)
        self.label_s.grid(row=10, column=2, padx=(55, 5), pady=5, sticky='w')
        self.input_s = tk.Entry(self.frame1, width=10, font=self.font_text)
        self.input_s.grid(row=10, column=3, padx=5, pady=5)
        self.input_s.insert(0, str(data.s))
        self.input_s.bind("<Return>", self.on_change)
        # n
        self.label_n = tk.Label(self.frame1, text="Sterberate T-Killerzellen (n):", font=self.font_text)
        self.label_n.grid(row=10, column=4, padx=(55, 5), pady=5, sticky='w')
        self.input_n = tk.Entry(self.frame1, width=10, font=self.font_text)
        self.input_n.grid(row=10, column=5, padx=5, pady=5)
        self.input_n.insert(0, str(data.n))
        self.input_n.bind("<Return>", self.on_change)
        # Plot Button
        self.button_plot = tk.Button(self.frame1, text="Start!", command=self.run1, font=self.font_text)
        self.button_plot.grid(row=11, column=5, padx=5, pady=(55, 5), sticky='w')
        self.button_plot.bind("<Return>", self.on_change)
        # Plot Button Immunantwort
        self.button_plot_2 = tk.Button(self.frame1, text="Start mit Immunantwort", command=self.run2,
                                       font=self.font_text)
        self.button_plot_2.grid(row=12, column=5, padx=5, pady=(15, 5), sticky='w')
        # Elemente anzeigen
        self.frame1.pack()
        # window main loop
        self.root.mainloop()

    def run1(self):
        self.on_change()
        plot_1()

    def run2(self):
        self.on_change()
        plot_2()

    def on_change(self, event_info=None):
        try:
            data.la = float(self.input_la.get())
            data.m = float(self.input_m.get())
            data.r = float(self.input_r.get())
            data.k = float(self.input_k.get())
            data.nu = float(self.input_nu.get())
            data.mu = float(self.input_mu.get())
            data.t = int(self.input_t.get())
            data.v_0 = float(self.input_v0.get())
            data.z_0 = float(self.input_z0.get())
            data.i_0 = float(self.input_i0.get())
            data.p_0 = float(self.input_p0.get())
            data.a = float(self.input_a.get())
            data.s = float(self.input_s.get())
            data.n = float(self.input_n.get())
        except ValueError:
            messagebox.showerror("Eingabefehler!", f" {ValueError}; Eingabe muss eine Fließkommazahl sein! (t: int)")
            return


def plot_1(window=None):
    t = np.arange(0, data.t, data.t / 60.0)
    # Warnungen zu "T" müssen ignoriert werden (Transpose Array)
    _data = black_box_2().T

    title = f'Simulation ( R = {reproduction():.2f} )'

    # Plotting
    fig = plt.figure(num=title, figsize=(15, 10), dpi=100)
    fig.tight_layout()
    ax1 = plt.subplot(211, projection='3d')
    ax2 = plt.subplot(337)
    ax3 = plt.subplot(338, sharey=ax2)
    ax4 = plt.subplot(339, sharey=ax3)
    fig.subplots_adjust(left=0.05, bottom=0.05, right=0.95, top=0.95, wspace=0.3, hspace=0.0)
    line, = ax1.plot3D(_data[0, :], _data[1, :], _data[2, :], color='blueviolet')
    line2 = ax2.plot(t, _data[0, :], 'blue')
    line3 = ax3.plot(t, _data[1, :], 'orange')
    line4 = ax4.plot(t, _data[2, :], 'green')
    ax1.set_xlabel('Viren', loc='left')
    ax1.set_ylabel('Gesunde Zellen', loc='top')
    ax1.set_zlabel('Infizierte Zellen')
    ax2.set_xlabel('Zeit')
    ax3.set_xlabel('Zeit')
    ax4.set_xlabel('Zeit')
    ax2.set_ylabel('Freie Viren')
    ax3.set_ylabel('Ges Zellen')
    ax4.set_ylabel('Inf Zellen')
    ax1.grid(True)
    ax2.grid(True)
    ax3.grid(True)
    ax4.grid(True)
    ani1 = animation.FuncAnimation(fig, update, 100, fargs=(_data, line), interval=1, blit=False)
    # ani1.save('matplot003.gif', writer='imagemagick')
    plt.show()


def plot_2():
    awp0 = [data.v_0, data.z_0, data.i_0, data.p_0]
    # t = np.linspace(0, 300, 50)
    t = np.arange(0, data.t, data.t / 60.0)
    awp = odeint(numeric_prep_3, awp0, t)

    v = awp[:, 0]
    z = awp[:, 1]
    i = awp[:, 2]
    p = awp[:, 3]

    tvzip = {'t': t, 'v': v, 'z': z, 'i': i, 'p': p}
    title = f"Simulation mit Immunantwort ( R = {reproduction():.2f} )"
    fig = plt.figure(num=title, figsize=(15, 10), dpi=100)
    plt.plot(tvzip["t"], tvzip["v"], 'blue', label="Anzahl V der freien Viren")
    plt.plot(tvzip["t"], tvzip["z"], 'orange', label="Anzahl Z der gesunden Zellen")
    plt.plot(tvzip["t"], tvzip["i"], 'green', label="Anzahl I der infizierten Zellen")
    plt.plot(tvzip["t"], tvzip["p"], 'black', label="Anzahl T der T-Killerzellen")
    plt.xlabel("Zeitachse t")
    # plt.title(f"Black Box ODE mit R={reproduction()}\n")
    plt.legend()
    plt.show()


def reproduction():
    """
    :return: reproduction rate R
    """
    return (data.k * data.r * data.la) / (data.m * data.mu * data.nu)


def numeric_prep(awp, t):
    v = awp[0]
    z = awp[1]
    i = awp[2]

    dVdt = data.k * i - data.nu * v
    dZdt = data.la - data.m * z + data.b * v - data.r * v * z
    dIdt = data.r * v * z - data.mu * i

    return [dVdt, dZdt, dIdt]


def numeric_prep_3(awp, t):
    v = awp[0]
    z = awp[1]
    i = awp[2]
    p = awp[3]

    dVdt = data.k * i - data.nu * v
    dZdt = data.la - data.m * z + data.b * v - data.r * v * z
    dIdt = data.r * v * z - data.mu * i - data.s * i * p
    dPdt = data.a * p * i - data.n * p

    return [dVdt, dZdt, dIdt, dPdt]


def black_box():
    # awp0 = [1000.0, float(data.la / data.m), 100.0]
    awp0 = [data.v_0, data.z_0, data.i_0]
    # t = np.linspace(0, 300, 50)
    t = np.arange(0, data.t, data.t / 60.0)
    awp = odeint(numeric_prep, awp0, t)

    v = awp[:, 0]
    z = awp[:, 1]
    i = awp[:, 2]

    return {"t": t, "v": v, "z": z, "i": i}


def black_box_2():
    # t = np.arange(0, 30, 0.5)
    t = np.arange(0, data.t, data.t / 60.0)
    # awp0 = [1000, 1000000, 100]
    awp0 = [data.v_0, data.z_0, data.i_0]
    out = odeint(numeric_prep, awp0, t)
    return out


def update(num, _data, _line):
    _line.set_data(_data[:2, :num])
    _line.set_3d_properties(_data[2, :num])


if __name__ == '__main__':
    # Instanz der Datenklasse Data erstellen
    data = Data()
    # Instanz der Klasse InputDataGUI erstellen, um GUI zu starten
    InputDataGUI()
