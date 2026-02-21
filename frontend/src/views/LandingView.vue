<template>
  <div class="fleet-landing">
    <nav class="fleet-nav">
      <div class="nav-wrap">
        <div class="nav-logo" @click="$router.push('/')">
          <Truck :size="24" />
          <span>FleetFlow</span>
        </div>
        <div class="nav-links">
          <a href="#features">Features</a>
          <a href="#how">Solutions</a>
          <a href="#stats">Pricing</a>
        </div>
        <div class="nav-btns">
          <button @click="$router.push('/login')" class="btn-text">Login</button>
          <button @click="$router.push('/signup')" class="btn-solid">Get Started</button>
        </div>
      </div>
    </nav>

    <section class="hero">
      <div class="badge">
        <span class="ping-dot"></span>
        <span>New: Real-Time Fleet Tracking & Analytics</span>
      </div>
      <h1>The Intelligence Behind<br/><span class="grad">Your Modern Fleet</span></h1>
      <p class="subtitle">Optimize delivery operations, ensure driver safety, and control finances with our modular logistics ecosystem.</p>
      <div class="hero-btns">
        <button @click="$router.push('/signup')" class="btn-hero">Start Free Trial <ArrowRight :size="16" /></button>
        <button @click="$router.push('/login')" class="btn-demo"><LogIn :size="18" /> Sign In</button>
      </div>
      <div class="dashboard-mock">
        <div class="mock-header">
          <div class="dots"><span></span><span></span><span></span></div>
        </div>
        <div class="mock-body">
          <div class="sidebar">
            <div class="sb-head">Active Units <span class="badge-sm">24</span></div>
            <div class="unit active"><div class="dot green"></div><div><div class="u-name">Truck #1042</div><div class="u-status">En route • 45m</div></div></div>
            <div class="unit"><div class="dot orange"></div><div><div class="u-name">Van #8821</div><div class="u-status">Maintenance Required</div></div></div>
            <div class="unit"><div class="dot green"></div><div><div class="u-name">Freight #3390</div><div class="u-status">Loading • Dock 4</div></div></div>
          </div>
          <div class="map-area">
            <div class="map-stat">
              <div class="stat-label">Fleet Efficiency</div>
              <div class="stat-value">94.2%</div>
              <div class="stat-trend"><TrendingUp :size="12" /> +2.4%</div>
            </div>
            <div class="map-marker"><Truck :size="24" /></div>
          </div>
        </div>
      </div>
      <div class="social-proof">
        <p>Trusted by forward-thinking logistics teams</p>
        <div class="logos">
          <span><Package :size="20" /> LOGISTICORP</span>
          <span><Truck :size="20" /> FASTFREIGHT</span>
          <span><Plane :size="20" /> AEROBOX</span>
        </div>
      </div>
    </section>

    <section id="features" class="features">
      <div class="section-head">
        <h3 class="tag">Modular Platform</h3>
        <h2>Everything needed to run a modern fleet</h2>
        <p>Our modular architecture allows you to enable exactly what you need.</p>
      </div>
      <div class="feature-grid">
        <div class="feature-card">
          <div class="f-icon blue"><Map :size="24" /></div>
          <h4>Command Center</h4>
          <p>Real-time visibility into every vehicle and driver with live GPS.</p>
        </div>
        <div class="feature-card">
          <div class="f-icon orange"><Route :size="24" /></div>
          <h4>Trip Dispatcher</h4>
          <p>AI-powered route optimization that adapts to traffic in real-time.</p>
        </div>
        <div class="feature-card">
          <div class="f-icon blue"><Wrench :size="24" /></div>
          <h4>Asset Management</h4>
          <p>Track maintenance schedules and prevent downtime before it happens.</p>
        </div>
        <div class="feature-card">
          <div class="f-icon blue"><BarChart3 :size="24" /></div>
          <h4>Financial Analytics</h4>
          <p>Deep dive into cost-per-mile, fuel usage, and revenue tracking.</p>
        </div>
      </div>
    </section>

    <section id="how" class="workflow">
      <div class="work-content">
        <div class="work-left">
          <h2>How FleetFlow Works</h2>
          <p>From intake to insight, we streamline every step of your logistics operation.</p>
        </div>
        <div class="work-steps">
          <div class="step"><div class="step-icon"><Upload :size="20" /></div><div><span>Step 1</span><h4>Vehicle Intake</h4><p>Quickly onboard new assets and drivers into the system.</p></div></div>
          <div class="step"><div class="step-icon"><Route :size="20" /></div><div><span>Step 2</span><h4>Route Planning</h4><p>Calculate the most efficient paths considering all constraints.</p></div></div>
          <div class="step"><div class="step-icon"><Satellite :size="20" /></div><div><span>Step 3</span><h4>Live Monitoring</h4><p>Watch your fleet move in real-time with instant alerts.</p></div></div>
          <div class="step"><div class="step-icon"><BarChart3 :size="20" /></div><div><span>Step 4</span><h4>Data Insights</h4><p>Automated reports generate actionable insights on performance.</p></div></div>
        </div>
      </div>
    </section>

    <section id="stats" class="stats">
      <div class="stat-item"><h3>10k+</h3><p>Vehicles Tracked</p></div>
      <div class="stat-item"><h3>99.9%</h3><p>Uptime Reliability</p></div>
      <div class="stat-item"><h3>25%</h3><p>Fuel Savings</p></div>
      <div class="stat-item"><h3>24/7</h3><p>Support Access</p></div>
    </section>

    <section class="cta-section">
      <div class="cta-box">
        <h2>Ready to optimize your fleet?</h2>
        <p>Join hundreds of logistics companies using FleetFlow to save costs and improve safety.</p>
        <div class="cta-btns">
          <button @click="$router.push('/signup')" class="btn-white">Get Started Now</button>
          <button class="btn-outline">Contact Sales</button>
        </div>
      </div>
    </section>

    <footer id="footer" class="footer">
      <div class="footer-content">
        <div class="footer-brand">
          <div class="f-logo"><Truck :size="20" /> FleetFlow</div>
          <p>The modern operating system for fleet management.</p>
        </div>
        <div class="footer-links">
          <div><h4>Product</h4><a href="#features">Features</a><a href="#">Pricing</a></div>
          <div><h4>Company</h4><a href="#">About</a><a href="#">Contact</a></div>
        </div>
      </div>
      <div class="footer-bottom">
        <p>© 2024 FleetFlow Inc. All rights reserved.</p>
      </div>
    </footer>
  </div>
</template>

<script setup lang="ts">
import { Truck, ArrowRight, LogIn, TrendingUp, Package, Plane, Map, Route, Wrench, BarChart3, Upload, Satellite } from 'lucide-vue-next';
</script>

<style scoped>
.fleet-landing { min-height: 100vh; background: #101922; color: #f1f5f9; font-family: 'Inter', sans-serif; }

/* Navigation */
.fleet-nav { position: fixed; top: 0; width: 100%; z-index: 50; background: rgba(16, 25, 34, 0.8); backdrop-filter: blur(12px); border-bottom: 1px solid #1e293b; }
.nav-wrap { max-width: 1280px; margin: 0 auto; padding: 0 2rem; display: flex; justify-content: space-between; align-items: center; height: 80px; }
.nav-logo { display: flex; align-items: center; gap: 12px; font-size: 20px; font-weight: 700; cursor: pointer; color: #fff; }
.nav-logo svg { color: #137fec; }
.nav-links { display: flex; gap: 32px; }
.nav-links a { color: #cbd5e1; font-size: 14px; font-weight: 500; text-decoration: none; transition: color 0.2s; }
.nav-links a:hover { color: #137fec; }
.nav-btns { display: flex; gap: 16px; align-items: center; }
.btn-text { background: none; border: none; color: #cbd5e1; font-size: 14px; font-weight: 600; cursor: pointer; padding: 8px 16px; transition: color 0.2s; }
.btn-text:hover { color: #fff; }
.btn-solid { background: #137fec; color: #fff; border: none; padding: 10px 20px; border-radius: 8px; font-size: 14px; font-weight: 600; cursor: pointer; box-shadow: 0 10px 15px -3px rgba(19, 127, 236, 0.25); transition: all 0.2s; }
.btn-solid:hover { background: #0d6edb; }

/* Hero */
.hero { max-width: 1280px; margin: 0 auto; padding: 140px 2rem 80px; text-align: center; }
.badge { display: inline-flex; align-items: center; gap: 8px; padding: 6px 12px; background: #1c242e; border: 1px solid rgba(71, 85, 105, 0.5); border-radius: 999px; font-size: 12px; color: #cbd5e1; margin-bottom: 32px; }
.ping-dot { position: relative; width: 8px; height: 8px; background: #f97316; border-radius: 50%; }
.ping-dot::before { content: ''; position: absolute; inset: 0; background: #f97316; border-radius: 50%; animation: ping 1s cubic-bezier(0, 0, 0.2, 1) infinite; }
@keyframes ping { 75%, 100% { transform: scale(2); opacity: 0; } }
.hero h1 { font-size: 56px; font-weight: 800; line-height: 1.1; margin-bottom: 24px; color: #fff; }
.grad { background: linear-gradient(to right, #137fec, #60a5fa); -webkit-background-clip: text; -webkit-text-fill-color: transparent; background-clip: text; }
.subtitle { font-size: 20px; color: #94a3b8; max-width: 700px; margin: 0 auto 40px; line-height: 1.6; }
.hero-btns { display: flex; gap: 16px; justify-content: center; margin-bottom: 64px; }
.btn-hero { background: #137fec; color: #fff; border: none; padding: 12px 32px; border-radius: 8px; font-size: 16px; font-weight: 700; cursor: pointer; display: flex; align-items: center; gap: 8px; box-shadow: 0 10px 15px -3px rgba(19, 127, 236, 0.3); transition: all 0.2s; }
.btn-hero:hover { background: #0d6edb; }
.btn-demo { background: #1c242e; color: #fff; border: 1px solid #475569; padding: 12px 32px; border-radius: 8px; font-size: 16px; font-weight: 700; cursor: pointer; display: flex; align-items: center; gap: 8px; transition: all 0.2s; }
.btn-demo:hover { background: #1e293b; }
.btn-demo svg { color: #cbd5e1; }

/* Dashboard Mock */
.dashboard-mock { max-width: 1200px; margin: 0 auto; border: 1px solid #1e293b; border-radius: 12px; background: rgba(28, 36, 46, 0.5); overflow: hidden; box-shadow: 0 0 120px -30px rgba(19, 127, 236, 0.3); }
.mock-header { height: 32px; background: #1c242e; border-bottom: 1px solid #1e293b; display: flex; align-items: center; padding: 0 16px; }
.dots { display: flex; gap: 8px; }
.dots span { width: 12px; height: 12px; border-radius: 50%; }
.dots span:nth-child(1) { background: #ef4444; }
.dots span:nth-child(2) { background: #eab308; }
.dots span:nth-child(3) { background: #22c55e; }
.mock-body { display: grid; grid-template-columns: 300px 1fr; min-height: 400px; }
.sidebar { background: rgba(16, 25, 34, 0.8); padding: 16px; border-right: 1px solid #1e293b; }
.sb-head { display: flex; justify-content: space-between; align-items: center; font-size: 12px; font-weight: 600; color: #94a3b8; text-transform: uppercase; margin-bottom: 16px; letter-spacing: 0.05em; }
.badge-sm { background: rgba(19, 127, 236, 0.2); color: #137fec; padding: 2px 8px; border-radius: 4px; font-size: 11px; font-weight: 700; }
.unit { display: flex; align-items: center; gap: 12px; padding: 12px; border-radius: 8px; margin-bottom: 8px; cursor: pointer; transition: background 0.2s; }
.unit.active { background: #1c242e; border: 1px solid rgba(71, 85, 105, 0.5); }
.unit:not(.active) { border: 1px solid transparent; }
.unit:hover { background: rgba(28, 36, 46, 0.5); }
.dot { width: 8px; height: 8px; border-radius: 50%; flex-shrink: 0; }
.dot.green { background: #4ade80; box-shadow: 0 0 8px rgba(74, 222, 128, 0.5); }
.dot.orange { background: #f97316; box-shadow: 0 0 8px rgba(249, 115, 22, 0.5); }
.u-name { font-size: 14px; font-weight: 500; color: #fff; }
.u-status { font-size: 12px; color: #64748b; }
.map-area { position: relative; background: #0f172a; display: flex; align-items: center; justify-content: center; }
.map-stat { position: absolute; top: 16px; right: 16px; background: rgba(28, 36, 46, 0.9); backdrop-filter: blur(8px); border: 1px solid #475569; padding: 12px; border-radius: 8px; }
.stat-label { font-size: 11px; color: #94a3b8; margin-bottom: 4px; }
.stat-value { font-size: 24px; font-weight: 700; color: #fff; }
.stat-trend { font-size: 11px; color: #4ade80; display: flex; align-items: center; gap: 4px; margin-top: 4px; }
.map-marker { width: 48px; height: 48px; background: #1c242e; border: 2px solid #137fec; border-radius: 50%; display: flex; align-items: center; justify-content: center; color: #137fec; position: relative; }
.map-marker::before { content: ''; position: absolute; inset: 0; background: rgba(19, 127, 236, 0.2); border-radius: 50%; animation: ping 2s cubic-bezier(0, 0, 0.2, 1) infinite; }

/* Social Proof */
.social-proof { margin-top: 64px; }
.social-proof p { font-size: 12px; font-weight: 500; color: #64748b; text-transform: uppercase; letter-spacing: 0.1em; margin-bottom: 24px; }
.logos { display: flex; justify-content: center; gap: 64px; flex-wrap: wrap; opacity: 0.5; transition: opacity 0.5s; }
.logos:hover { opacity: 1; }
.logos span { display: flex; align-items: center; gap: 8px; font-size: 18px; font-weight: 700; color: #fff; }

/* Features */
.features { padding: 80px 2rem; background: #101922; border-top: 1px solid #1e293b; }
.section-head { text-align: center; margin-bottom: 64px; max-width: 800px; margin-left: auto; margin-right: auto; }
.tag { color: #137fec; font-size: 12px; font-weight: 700; text-transform: uppercase; letter-spacing: 0.1em; margin-bottom: 8px; }
.section-head h2 { font-size: 36px; font-weight: 800; color: #fff; margin-bottom: 16px; }
.section-head p { font-size: 18px; color: #94a3b8; }
.feature-grid { max-width: 1280px; margin: 0 auto; display: grid; grid-template-columns: repeat(auto-fit, minmax(280px, 1fr)); gap: 24px; }
.feature-card { background: #1c242e; border: 1px solid #1e293b; border-radius: 12px; padding: 24px; transition: all 0.3s; cursor: pointer; }
.feature-card:hover { border-color: rgba(19, 127, 236, 0.5); box-shadow: 0 0 30px -10px rgba(19, 127, 236, 0.3); }
.f-icon { width: 48px; height: 48px; border-radius: 8px; display: flex; align-items: center; justify-content: center; margin-bottom: 16px; transition: all 0.3s; }
.f-icon.blue { background: rgba(19, 127, 236, 0.1); color: #137fec; }
.f-icon.orange { background: rgba(249, 115, 22, 0.1); color: #f97316; }
.feature-card:hover .f-icon.blue { background: #137fec; color: #fff; }
.feature-card:hover .f-icon.orange { background: #f97316; color: #fff; }
.feature-card h4 { font-size: 18px; font-weight: 700; color: #fff; margin-bottom: 8px; }
.feature-card p { font-size: 14px; color: #94a3b8; line-height: 1.6; }

/* Workflow */
.workflow { padding: 80px 2rem; background: #0d131a; }
.work-content { max-width: 1280px; margin: 0 auto; display: grid; grid-template-columns: 1fr 2fr; gap: 48px; }
.work-left h2 { font-size: 32px; font-weight: 800; color: #fff; margin-bottom: 24px; }
.work-left p { font-size: 18px; color: #94a3b8; line-height: 1.6; }
.work-steps { border-left: 2px solid #1e293b; padding-left: 32px; display: flex; flex-direction: column; gap: 48px; }
.step { display: flex; gap: 16px; position: relative; }
.step::before { content: ''; position: absolute; left: -40px; top: 0; width: 16px; height: 16px; background: #1c242e; border: 2px solid #475569; border-radius: 50%; transition: all 0.3s; }
.step:hover::before { border-color: #137fec; background: #137fec; }
.step-icon { width: 48px; height: 48px; background: #1c242e; border: 1px solid #475569; border-radius: 8px; display: flex; align-items: center; justify-content: center; color: #fff; flex-shrink: 0; }
.step span { display: block; font-size: 11px; font-weight: 700; color: #64748b; text-transform: uppercase; letter-spacing: 0.05em; margin-bottom: 4px; }
.step h4 { font-size: 20px; font-weight: 700; color: #fff; margin-bottom: 8px; }
.step p { font-size: 14px; color: #94a3b8; line-height: 1.6; }

/* Stats */
.stats { padding: 64px 2rem; background: #1c242e; border-top: 1px solid #1e293b; border-bottom: 1px solid #1e293b; display: grid; grid-template-columns: repeat(auto-fit, minmax(200px, 1fr)); gap: 32px; max-width: 1280px; margin: 0 auto; text-align: center; }
.stat-item h3 { font-size: 40px; font-weight: 900; color: #fff; margin-bottom: 8px; }
.stat-item p { font-size: 14px; font-weight: 500; color: #64748b; }

/* CTA */
.cta-section { padding: 96px 2rem; }
.cta-box { max-width: 1000px; margin: 0 auto; background: linear-gradient(to bottom right, #1e3a8a, #1e293b); border: 1px solid #475569; border-radius: 24px; padding: 64px 32px; text-align: center; position: relative; overflow: hidden; }
.cta-box::before { content: ''; position: absolute; top: -80px; right: -80px; width: 320px; height: 320px; background: rgba(19, 127, 236, 0.2); border-radius: 50%; filter: blur(60px); }
.cta-box::after { content: ''; position: absolute; bottom: -80px; left: -80px; width: 320px; height: 320px; background: rgba(249, 115, 22, 0.1); border-radius: 50%; filter: blur(60px); }
.cta-box h2 { font-size: 40px; font-weight: 700; color: #fff; margin-bottom: 16px; position: relative; z-index: 1; }
.cta-box p { font-size: 18px; color: #cbd5e1; margin-bottom: 40px; position: relative; z-index: 1; }
.cta-btns { display: flex; gap: 16px; justify-content: center; position: relative; z-index: 1; }
.btn-white { background: #fff; color: #0f172a; border: none; padding: 12px 32px; border-radius: 8px; font-size: 16px; font-weight: 700; cursor: pointer; transition: all 0.2s; }
.btn-white:hover { background: #f1f5f9; }
.btn-outline { background: transparent; color: #fff; border: 1px solid rgba(255, 255, 255, 0.3); padding: 12px 32px; border-radius: 8px; font-size: 16px; font-weight: 700; cursor: pointer; transition: all 0.2s; }
.btn-outline:hover { background: rgba(255, 255, 255, 0.1); }

/* Footer */
.footer { background: #0b1118; border-top: 1px solid #1e293b; padding: 64px 2rem 32px; }
.footer-content { max-width: 1280px; margin: 0 auto; display: grid; grid-template-columns: 2fr 1fr; gap: 48px; margin-bottom: 48px; }
.footer-brand { }
.f-logo { display: flex; align-items: center; gap: 8px; font-size: 20px; font-weight: 700; color: #fff; margin-bottom: 16px; }
.f-logo svg { color: #137fec; }
.footer-brand p { font-size: 14px; color: #64748b; max-width: 300px; }
.footer-links { display: grid; grid-template-columns: 1fr 1fr; gap: 32px; }
.footer-links h4 { font-size: 14px; font-weight: 700; color: #fff; margin-bottom: 16px; }
.footer-links a { display: block; font-size: 14px; color: #94a3b8; text-decoration: none; margin-bottom: 8px; transition: color 0.2s; }
.footer-links a:hover { color: #137fec; }
.footer-bottom { max-width: 1280px; margin: 0 auto; padding-top: 32px; border-top: 1px solid #1e293b; text-align: center; font-size: 14px; color: #64748b; }

@media (max-width: 768px) {
  .nav-links { display: none; }
  .hero h1 { font-size: 36px; }
  .mock-body { grid-template-columns: 1fr; }
  .sidebar { display: none; }
  .work-content { grid-template-columns: 1fr; }
  .footer-content { grid-template-columns: 1fr; }
}
</style>
