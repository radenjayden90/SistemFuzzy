document.getElementById("sleepForm").addEventListener("submit", async function(e){
    e.preventDefault();

    const durasi = document.getElementById("durasi").value;
    const gangguan = document.getElementById("gangguan").value;
    const konsistensi = document.getElementById("konsistensi").value;
    const stres = document.getElementById("stres").value;

    const btnText = document.querySelector(".btn-text");
    const loader = document.querySelector(".loader");
    const submitBtn = document.getElementById("submitBtn");
    const hasilBox = document.getElementById("hasilBox");
    
    // UI Loading State
    btnText.style.display = "none";
    loader.style.display = "block";
    submitBtn.disabled = true;

    try {
        const res = await fetch("http://localhost:5000/fuzzy", {
            method: "POST",
            headers: {"Content-Type": "application/json"},
            body: JSON.stringify({durasi, gangguan, konsistensi, stres})
        });

        if (!res.ok) throw new Error("Terjadi kesalahan pada server");
        
        const data = await res.json();
        
        // Hide Loader
        btnText.style.display = "block";
        loader.style.display = "none";
        submitBtn.disabled = false;

        // Show Result
        hasilBox.classList.remove("hidden");
        
        // Update Ring Dashboard (max score 10)
        // Stroke dasharray format: "value, 100" (percentage)
        const percentage = (data.kualitas_tidur / 10) * 100;
        document.getElementById("scoreCircle").setAttribute("stroke-dasharray", `${percentage}, 100`);
        document.getElementById("scoreText").textContent = data.kualitas_tidur.toFixed(2);
        
        let colorClass = "cyan";
        if (data.kualitas_tidur <= 4) colorClass = "red";
        else if (data.kualitas_tidur < 7) colorClass = "orange";
        
        const svg = document.querySelector(".circular-chart");
        svg.className.baseVal = `circular-chart ${colorClass}`;
        
        // Set Kategori status
        document.getElementById("kategoriText").textContent = data.kategori;

    } catch (error) {
        alert(error.message);
        btnText.style.display = "block";
        loader.style.display = "none";
        submitBtn.disabled = false;
    }
});