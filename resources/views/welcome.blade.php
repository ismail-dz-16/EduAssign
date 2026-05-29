@extends('layouts.app')

@section('content')
<div class="landing-page">
    
    {{-- HERO SECTION --}}
    <header class="hero">
        <div class="hero-content">
            <span class="announcement">🚀 Now Open for INSFP Students</span>
            <h1>Master Your Assignments with <span>EduAssign</span></h1>
            <p>The all-in-one platform for teachers to create interactive tasks and students to submit work seamlessly. Built for speed, designed for clarity.</p>
            
            <div class="hero-btns">
                @auth
                    <a href="{{ auth()->user()->role === 'teacher' ? route('teacher.dashboard') : route('student.dashboard') }}" class="btn-primary btn-lg">Go to Dashboard</a>
                @else
                    <a href="{{ route('register') }}" class="btn-primary btn-lg">Get Started for Free</a>
                    <a href="#features" class="btn-secondary btn-lg">Learn More</a>
                @endauth
            </div>
        </div>
        <div class="hero-visual">
            <div class="abstract-shape"></div>
        </div>
    </header>

    {{-- FEATURES SECTION --}}
    <section id="features" class="section">
        <div class="section-head text-center">
            <h2>Everything you need to <span>succeed</span></h2>
            <p>Powerful tools designed to make academic management effortless.</p>
        </div>

        <div class="features-grid">
            <div class="feature-card">
                <div class="f-icon">📝</div>
                <h3>Dynamic Builder</h3>
                <p>Create assignments with multiple choice, short answers, and more in seconds.</p>
            </div>

            <div class="feature-card">
                <div class="f-icon">📊</div>
                <h3>Live Tracking</h3>
                <p>Teachers can track submissions in real-time and manage student progress easily.</p>
            </div>

            <div class="feature-card">
                <div class="f-icon">🔒</div>
                <h3>Secure & Private</h3>
                <p>Your data is protected. Built with modern security standards for peace of mind.</p>
            </div>

            <div class="feature-card">
                <div class="f-icon">📱</div>
                <h3>Fully Responsive</h3>
                <p>Access your assignments from any device—phone, tablet, or desktop.</p>
            </div>
        </div>
    </section>

    {{-- STATS / PROOF SECTION --}}
    <section class="stats-bar">
        <div class="stat-item">
            <span class="stat-num">100%</span>
            <span class="stat-label">Digital</span>
        </div>
        <div class="stat-item">
            <span class="stat-num">Fast</span>
            <span class="stat-label">Performance</span>
        </div>
        <div class="stat-item">
            <span class="stat-num">Easy</span>
            <span class="stat-label">UX Design</span>
        </div>
    </section>

    {{-- CTA SECTION --}}
    <section class="final-cta">
        <div class="cta-card">
            <h2>Ready to transform your classroom?</h2>
            <p>Join EduAssign today and start managing assignments like a pro.</p>
            <a href="{{ route('register') }}" class="btn-primary btn-lg">Join Now</a>
        </div>
    </section>

</div>
@endsection