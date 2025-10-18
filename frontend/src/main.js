// API Base URL
const API_BASE = 'http://127.0.0.1:8080';

// Dashboard Component
function intelligenceDashboard() {
    return {
        currentView: 'dashboard',
        currentIdea: 'AI-Powered Audio File Organization & Metadata Management',
        dataConfidence: 87,
        marketConfidence: 87,
        analysisRunning: false,
        painPoints: [],
        competitors: null,
        socialIntel: null,
        selectedScenario: 'moderate_scenario',
        selectedStrategy: 'calendar',
        framework: null,
        selectedPainPoint: null,
        videoConcepts: null,
        audioIntelligence: null,
        angelInvestors: null,
        selectedInvestorCategory: 'all',
        affiliatePartners: null,
        selectedAffiliateCategory: 'all',
        contactedPartners: new Set(JSON.parse(localStorage.getItem('contactedPartners') || '[]')),
        partnerEmailVariants: JSON.parse(localStorage.getItem('partnerEmailVariants') || '{}'),
        contactedInvestors: new Set(JSON.parse(localStorage.getItem('contactedInvestors') || '[]')),
        investorEmailVariants: JSON.parse(localStorage.getItem('investorEmailVariants') || '{}'),
        financialData: null,
        competitorOverview: null,
        competitorRankings: null,
        selectedCompetitor: null,
        competitorAnalysis: null,
        loadingCompetitors: false,
        
        // Real TAM/SAM/SOM data
        tamValue: 1840000000,
        samValue: 772800000,
        somValue: 11592000,
        tamConfidence: 89,
        samConfidence: 84,
        somConfidence: 76,
        overallConfidence: 86,
        totalCompetitors: 30,
        topThreat: 'Splice (95)',

        formatCurrency(value) {
            if (value >= 1000000000) {
                return '$' + (value / 1000000000).toFixed(1) + 'B';
            } else if (value >= 1000000) {
                return '$' + (value / 1000000).toFixed(0) + 'M';
            }
            return '$' + value.toLocaleString();
        },

        getConfidenceLevel(confidence) {
            if (confidence >= 90) return 'Very High';
            if (confidence >= 80) return 'High Accuracy';
            return 'Good';
        },

        getViewTitle() {
            const titles = {
                'dashboard': 'Intelligence Dashboard',
                'competitors': 'Competitor Intelligence',
                'pain-points': 'Pain Point Analysis',
                'social-intel': 'Social Intelligence',
                'financial': 'Financial Projections',
                'marketing-videos': 'Marketing Videos',
                'audio-intelligence': 'Audio Intelligence',
                'angel-investors': 'Angel Investors',
                'affiliate-partners': 'Affiliate Partners'
            };
            return titles[this.currentView] || 'Dashboard';
        },

        switchView(view) {
            this.currentView = view;
            if (view === 'pain-points' && this.painPoints.length === 0) {
                this.loadPainPoints();
            }
            if (view === 'competitors' && !this.competitorOverview) {
                this.loadCompetitorOverview();
                this.loadCompetitorRankings();
            }
            if (view === 'social-intel' && !this.socialIntel) {
                this.loadSocialIntelligence();
            }
            if (view === 'financial' && !this.financialData) {
                this.loadFinancialIntelligence();
            }
            if (view === 'marketing-videos' && this.videoConcepts.length === 0) {
                this.generateVideoConcepts();
            }
            if (view === 'audio-intelligence' && !this.audioIntelligence) {
                this.loadAudioIntelligence();
            }
            if (view === 'angel-investors' && !this.angelInvestors) {
                this.loadAngelInvestors();
            }
            if (view === 'affiliate-partners') {
                if (!this.affiliatePartners || this.affiliatePartners.length === 0) {
                    this.loadAffiliatePartners();
                }
            }
        },

        async loadPainPoints() {
            try {
                const response = await fetch(`${API_BASE}/api/pain-points`);
                const data = await response.json();
                if (data.success && data.pain_points && data.pain_points.audio_professionals) {
                    this.painPoints = data.pain_points.audio_professionals.top_pain_points.map(pp => ({
                        name: pp.pain,
                        pain_score: pp.severity,
                        affected_users: Math.round(pp.frequency / 3) + '%',
                        market_gap: pp.market_gap,
                        solutions: pp.solutions
                    }));
                } else {
                    this.painPoints = Array.isArray(data.categories) ? data.categories : [];
                }
                if (!this.selectedPainPoint && this.painPoints.length > 0) {
                    this.selectedPainPoint = this.painPoints[0].name;
                }
            } catch (err) {
                console.error('Failed to load pain points:', err);
                this.painPoints = [
                    { name: 'Metadata and asset organization chaos', pain_score: 92, affected_users: '89%' },
                    { name: 'Background noise and environmental interference', pain_score: 92, affected_users: '84%' },
                    { name: 'Audio consistently underprioritized in budgets', pain_score: 90, affected_users: '78%' }
                ];
                if (!this.selectedPainPoint) this.selectedPainPoint = this.painPoints[0].name;
            }
        },

        loadSocialIntelQuick() {
            this.socialIntel = {
                reddit_mentions: 15420,
                twitter_mentions: 8500,
                youtube_uploads: 127
            };
        },

        loadFrameworkQuick() {
            this.framework = {
                cac: 710,
                ltv: 2130,
                ratio: 3.0
            };
        },

        async loadCompetitors() {
            try {
                const response = await fetch(`${API_BASE}/api/competitors-enhanced`);
                const data = await response.json();
                this.competitors = data.competitors || [];
            } catch (err) {
                console.error('Failed to load competitors:', err);
                // Fallback competitor data
                this.competitors = [
                    {
                        name: 'Splice',
                        category: 'Sample Library',
                        threat_score: 95,
                        market_share: 15.2,
                        funding: '$57.5M',
                        arr: '$45M',
                        users: '4M+',
                        strengths: ['Massive Library', 'AI Features', 'Brand Recognition'],
                        weaknesses: ['High Cost', 'Limited Organization', 'Subscription Only']
                    },
                    {
                        name: 'Loopmasters',
                        category: 'Sample Packs',
                        threat_score: 78,
                        market_share: 8.5,
                        funding: '$12M',
                        arr: '$18M',
                        users: '1.2M+',
                        strengths: ['Quality Content', 'Artist Partnerships', 'Genre Variety'],
                        weaknesses: ['Poor Search', 'No AI', 'Outdated UI']
                    },
                    {
                        name: 'Native Instruments',
                        category: 'Audio Software',
                        threat_score: 85,
                        market_share: 12.8,
                        funding: 'Private',
                        arr: '$120M',
                        users: '2.5M+',
                        strengths: ['Hardware Integration', 'Professional Tools', 'Established Brand'],
                        weaknesses: ['Complex UI', 'Expensive', 'Learning Curve']
                    },
                    {
                        name: 'Output',
                        category: 'Creative Software',
                        threat_score: 72,
                        market_share: 6.3,
                        funding: '$45M',
                        arr: '$25M',
                        users: '800K+',
                        strengths: ['Modern UI', 'Creative Focus', 'Innovation'],
                        weaknesses: ['Limited Library', 'High Price', 'Resource Heavy']
                    },
                    {
                        name: 'Beatport',
                        category: 'Music Platform',
                        threat_score: 65,
                        market_share: 4.2,
                        funding: '$30M',
                        arr: '$15M',
                        users: '1.5M+',
                        strengths: ['DJ Focus', 'High Quality', 'Industry Connections'],
                        weaknesses: ['Niche Market', 'Limited Tools', 'No Organization']
                    },
                    {
                        name: 'Ableton',
                        category: 'DAW + Samples',
                        threat_score: 88,
                        market_share: 18.5,
                        funding: 'Private',
                        arr: '$85M',
                        users: '2M+',
                        strengths: ['Integrated DAW', 'Live Performance', 'Strong Community'],
                        weaknesses: ['Complex Setup', 'Learning Curve', 'Mac/PC Only']
                    }
                ];
            }
        },

        getThreatLevel(score) {
            if (score >= 90) return 'Critical';
            if (score >= 80) return 'High';
            if (score >= 70) return 'Medium';
            if (score >= 60) return 'Low';
            return 'Minimal';
        },

        getThreatColor(score) {
            if (score >= 90) return 'bg-red-500/20 text-red-400';
            if (score >= 80) return 'bg-orange-500/20 text-orange-400';
            if (score >= 70) return 'bg-yellow-500/20 text-yellow-400';
            if (score >= 60) return 'bg-blue-500/20 text-blue-400';
            return 'bg-green-500/20 text-green-400';
        },

        getThreatTextColor(score) {
            if (score >= 90) return 'text-red-400';
            if (score >= 80) return 'text-orange-400';
            if (score >= 70) return 'text-yellow-400';
            if (score >= 60) return 'text-blue-400';
            return 'text-green-400';
        },

        getThreatBorderColor(score) {
            if (score >= 90) return 'border-red-500/30';
            if (score >= 80) return 'border-orange-500/30';
            if (score >= 70) return 'border-yellow-500/30';
            if (score >= 60) return 'border-blue-500/30';
            return 'border-green-500/30';
        },

        getThreatBarColor(score) {
            if (score >= 90) return 'bg-red-500';
            if (score >= 80) return 'bg-orange-500';
            if (score >= 70) return 'bg-yellow-500';
            if (score >= 60) return 'bg-blue-500';
            return 'bg-green-500';
        },

        async loadSocialIntelligence() {
            try {
                const response = await fetch(`${API_BASE}/api/social-intelligence`);
                const data = await response.json();
                
                if (data.success) {
                    this.socialIntel = data.social_intelligence;
                    const totalMentions = (data.social_intelligence.platform_analysis.reddit.audio_discussions || 0) + 
                                         (data.social_intelligence.platform_analysis.twitter.audio_professionals || 0) + 
                                         (data.social_intelligence.platform_analysis.youtube.audio_tutorials || 0);
                    alert('🔥 Social Intelligence loaded! ' + totalMentions + ' mentions analyzed across all platforms.');
                } else {
                    alert('❌ Failed to load social intelligence: ' + data.error);
                }
            } catch (err) {
                console.error('Failed to load social intelligence:', err);
                alert('❌ Network error loading social intelligence');
            }
        },

        getSentimentScore() {
            if (!this.socialIntel?.sentiment_analysis) return '42.3';
            const positive = this.socialIntel.sentiment_analysis.positive || 0;
            const negative = this.socialIntel.sentiment_analysis.negative || 0;
            return ((positive - negative + 100) / 2).toFixed(1);
        },

        getPlatformColor(platform) {
            const colors = {
                'reddit': 'bg-orange-500/20',
                'twitter': 'bg-blue-500/20',
                'youtube': 'bg-red-500/20',
                'google_trends': 'bg-green-500/20',
                'websites': 'bg-purple-500/20',
                'forums': 'bg-yellow-500/20'
            };
            return colors[platform] || 'bg-gray-500/20';
        },

        getPlatformIcon(platform) {
            const icons = {
                'reddit': 'fab fa-reddit',
                'twitter': 'fab fa-twitter',
                'youtube': 'fab fa-youtube',
                'google_trends': 'fas fa-chart-line',
                'websites': 'fas fa-globe',
                'forums': 'fas fa-comments'
            };
            return icons[platform] || 'fas fa-circle';
        },

        formatTimeAgo(timestamp) {
            const now = new Date();
            const time = new Date(timestamp);
            const diffInHours = Math.floor((now - time) / (1000 * 60 * 60));
            
            if (diffInHours < 1) return 'Just now';
            if (diffInHours < 24) return `${diffInHours}h ago`;
            const diffInDays = Math.floor(diffInHours / 24);
            return `${diffInDays}d ago`;
        },

        async loadFinancialIntelligence() {
            try {
                const response = await fetch(`${API_BASE}/api/financial-intelligence`);
                const data = await response.json();
                
                if (data.success) {
                    this.financialData = data.financial_intelligence;
                    this.initializeRevenueChart();
                    const pricingTiers = Object.keys(data.financial_intelligence.pricing_strategy || {}).length;
                    alert('💰 Financial Intelligence loaded! 5-year projections ready with ' + pricingTiers + ' pricing tiers.');
                } else {
                    alert('❌ Failed to load financial intelligence: ' + data.error);
                }
            } catch (err) {
                console.error('Failed to load financial intelligence:', err);
                alert('❌ Network error loading financial intelligence');
            }
        },

        getPricingTierColor(tierName) {
            const colors = {
                'starter': 'text-blue-400',
                'professional': 'text-purple-400',
                'enterprise': 'text-orange-400'
            };
            return colors[tierName] || 'text-gray-400';
        },

        getPricingTierBorder(tierName) {
            const borders = {
                'starter': 'border-blue-500/30',
                'professional': 'border-purple-500/30',
                'enterprise': 'border-orange-500/30'
            };
            return borders[tierName] || 'border-gray-500/30';
        },

        getSelectedProjection() {
            if (!this.financialData?.revenue_projections?.[this.selectedScenario]) return null;
            const scenario = this.financialData.revenue_projections[this.selectedScenario];
            return {
                total_revenue: scenario.year_5?.revenue || 0,
                total_users: scenario.year_5?.customers || 0,
                arpu: scenario.year_5?.arpu || 0
            };
        },

        calculateMarketShare() {
            const projection = this.getSelectedProjection();
            if (!projection || !this.financialData?.market_analysis?.serviceable_obtainable_market) return '0.0';
            const marketSize = this.financialData.market_analysis.serviceable_obtainable_market;
            return ((projection.total_revenue / marketSize) * 100).toFixed(2);
        },

        getCAC() {
            return this.financialData?.market_analysis?.user_acquisition_cost?.organic?.cac || 28;
        },

        getLTVCACColor(ltv, cac) {
            const ratio = ltv / cac;
            if (ratio >= 5) return 'text-green-400';
            if (ratio >= 3) return 'text-yellow-400';
            return 'text-red-400';
        },

        initializeRevenueChart() {
            setTimeout(() => {
                const ctx = document.getElementById('revenueProjectionChart');
                if (ctx && this.financialData?.revenue_projections) {
                    const moderate = this.financialData.revenue_projections.moderate_scenario;
                    const aggressive = this.financialData.revenue_projections.aggressive_scenario;
                    const conservative = this.financialData.revenue_projections.conservative_scenario;

                    // Convert object format to array
                    const moderateData = [moderate.year_1.revenue, moderate.year_2.revenue, moderate.year_3.revenue, moderate.year_4.revenue, moderate.year_5.revenue].map(v => v / 1000000);
                    const aggressiveData = [aggressive.year_1.revenue, aggressive.year_2.revenue, aggressive.year_3.revenue, aggressive.year_4.revenue, aggressive.year_5.revenue].map(v => v / 1000000);
                    const conservativeData = [conservative.year_1.revenue, conservative.year_2.revenue, conservative.year_3.revenue, conservative.year_4.revenue, conservative.year_5.revenue].map(v => v / 1000000);

                    new Chart(ctx, {
                        type: 'line',
                        data: {
                            labels: ['Year 1', 'Year 2', 'Year 3', 'Year 4', 'Year 5'],
                            datasets: [
                                {
                                    label: 'Conservative',
                                    data: conservativeData,
                                    borderColor: '#eab308',
                                    backgroundColor: 'rgba(234, 179, 8, 0.1)',
                                    tension: 0.4
                                },
                                {
                                    label: 'Moderate',
                                    data: moderateData,
                                    borderColor: '#3b82f6',
                                    backgroundColor: 'rgba(59, 130, 246, 0.1)',
                                    tension: 0.4
                                },
                                {
                                    label: 'Aggressive',
                                    data: aggressiveData,
                                    borderColor: '#10b981',
                                    backgroundColor: 'rgba(16, 185, 129, 0.1)',
                                    tension: 0.4
                                }
                            ]
                        },
                        options: {
                            responsive: true,
                            maintainAspectRatio: false,
                            plugins: {
                                legend: {
                                    labels: { color: '#9ca3af' }
                                }
                            },
                            scales: {
                                y: {
                                    beginAtZero: true,
                                    grid: { color: 'rgba(255, 255, 255, 0.1)' },
                                    ticks: { 
                                        color: '#9ca3af',
                                        callback: function(value) {
                                            return '$' + value + 'M';
                                        }
                                    }
                                },
                                x: {
                                    grid: { color: 'rgba(255, 255, 255, 0.1)' },
                                    ticks: { color: '#9ca3af' }
                                }
                            }
                        }
                    });
                }
            }, 100);
        },

        async generateVideoConcepts() {
            try {
                const response = await fetch(`${API_BASE}/api/generate-video-concepts`, {
                    method: 'POST',
                    headers: { 'Content-Type': 'application/json' },
                    body: JSON.stringify({ count: 3 })
                });
                const data = await response.json();
                
                if (data.success) {
                    // Initialize flags so buttons render correctly
                    this.videoConcepts = (data.concepts || []).map(c => ({
                        ...c,
                        generating_sora: false,
                        generating_gemini: false
                    }));
                    alert('🎬 Generated ' + data.total_concepts + ' viral video concepts based on real pain points!');
                } else {
                    alert('❌ Failed to generate video concepts: ' + data.error);
                }
            } catch (err) {
                console.error('Failed to generate video concepts:', err);
                alert('❌ Network error generating video concepts');
            }
        },

        async regenerateConcept(conceptId, painPointCategory) {
            try {
                const response = await fetch(`${API_BASE}/api/regenerate-concept`, {
                    method: 'POST',
                    headers: { 'Content-Type': 'application/json' },
                    body: JSON.stringify({ 
                        concept_id: conceptId,
                        pain_point_category: painPointCategory 
                    })
                });
                const data = await response.json();
                
                if (data.success) {
                    // Replace the concept in the array
                    const index = this.videoConcepts.findIndex(c => c.id === conceptId);
                    if (index !== -1) {
                        this.videoConcepts[index] = {
                            ...data.concept,
                            generating_sora: false,
                            generating_gemini: false
                        };
                    }
                    alert('🔄 Concept regenerated with new viral hook!');
                } else {
                    alert('❌ Failed to regenerate concept: ' + data.error);
                }
            } catch (err) {
                console.error('Failed to regenerate concept:', err);
                alert('❌ Network error regenerating concept');
            }
        },

        async generateSoraVideo(concept) {
            if (!concept || concept.generating_sora) { return; }
            alert('🎥 Sora button clicked! Concept ID: ' + (concept.id || 'unknown'));
            console.log('🎥 Generating Sora video for concept:', concept.id);
            concept.generating_sora = true;
            try {
                const response = await fetch(`${API_BASE}/api/generate-sora-video`, {
                    method: 'POST',
                    headers: { 'Content-Type': 'application/json' },
                    body: JSON.stringify({ 
                        prompt: concept.sora_prompt,
                        concept_id: concept.id
                    })
                });
                const data = await response.json();
                
                if (data.success) {
                    concept.sora_video = data.video;
                    alert('🎥 Sora video generated successfully!\n\n' + 
                          '📁 File: ' + data.video.video_id + '\n' +
                          '📊 Size: ' + data.video.file_size + '\n' +
                          '⏱️ Duration: ' + data.video.duration + 's\n' +
                          '🎬 Ready for preview and download!');
                } else {
                    alert('❌ Failed to generate Sora video: ' + data.error);
                }
            } catch (err) {
                console.error('Failed to generate Sora video:', err);
                alert('❌ Network error generating Sora video');
            } finally {
                concept.generating_sora = false;
            }
        },

        async generateGeminiVideo(concept) {
            if (!concept || concept.generating_gemini) { return; }
            alert('🎬 Gemini button clicked! Concept ID: ' + (concept.id || 'unknown'));
            console.log('🎬 Generating Gemini video for concept:', concept.id);
            concept.generating_gemini = true;
            try {
                const response = await fetch(`${API_BASE}/api/generate-gemini-video`, {
                    method: 'POST',
                    headers: { 'Content-Type': 'application/json' },
                    body: JSON.stringify({ 
                        prompt: concept.gemini_prompt,
                        concept_id: concept.id
                    })
                });
                const data = await response.json();
                
                if (data.success) {
                    concept.gemini_video = data.video;
                    alert('🎬 Gemini video generated successfully!\n\n' + 
                          '📁 File: ' + data.video.video_id + '\n' +
                          '📊 Size: ' + data.video.file_size + '\n' +
                          '⏱️ Duration: ' + data.video.duration + 's\n' +
                          '🎬 Ready for preview and download!');
                } else {
                    alert('❌ Failed to generate Gemini video: ' + data.error);
                }
            } catch (err) {
                console.error('Failed to generate Gemini video:', err);
                alert('❌ Network error generating Gemini video');
            } finally {
                concept.generating_gemini = false;
            }
        },

        copyToClipboard(text) {
            navigator.clipboard.writeText(text).then(() => {
                alert('📋 Prompt copied to clipboard!');
            }).catch(() => {
                alert('❌ Failed to copy to clipboard');
            });
        },

        downloadVideo(video) {
            // Create download link and trigger download
            const link = document.createElement('a');
            const href = (video && typeof video.video_url === 'string' && video.video_url.startsWith('http'))
                ? video.video_url
                : `${API_BASE}${video.video_url}`;
            link.href = href;
            link.download = `${video.video_id}.mp4`;
            link.target = '_blank';
            document.body.appendChild(link);
            link.click();
            document.body.removeChild(link);
            
            alert('⬇️ Downloading ' + video.video_id + ' (' + video.file_size + ')');
        },

        previewVideo(video) {
            // Open video in new tab for preview
            const href = (video && typeof video.video_url === 'string' && video.video_url.startsWith('http'))
                ? video.video_url
                : `${API_BASE}${video.video_url}`;
            window.open(href, '_blank');
        },

        async loadAudioIntelligence() {
            try {
                console.log('🎵 Loading audio industry intelligence...');
                const response = await fetch(`${API_BASE}/api/audio-industry-intelligence`, {
                    method: 'POST',
                    headers: { 'Content-Type': 'application/json' },
                    body: JSON.stringify({})
                });
                const data = await response.json();
                
                if (data.success) {
                    this.audioIntelligence = data.audio_intelligence;
                    console.log('✅ Audio intelligence loaded:', this.audioIntelligence);
                    console.log('Opportunity Score:', this.audioIntelligence?.overall_opportunity_score);
                } else {
                    console.error('❌ Failed to load audio intelligence:', data.error);
                }
            } catch (error) {
                console.error('❌ Audio intelligence error:', error);
            }
        },

        async loadAngelInvestors(category = 'all') {
            try {
                console.log('💰 Loading angel investors...');
                const response = await fetch(`${API_BASE}/api/angel-investors?category=${category}`);
                const data = await response.json();
                
                if (data.success) {
                    this.angelInvestors = data.angel_investors;
                    this.selectedInvestorCategory = category;
                    console.log(`✅ Loaded ${data.total_count} angel investors`);
                } else {
                    console.error('❌ Failed to load angel investors:', data.error);
                    alert('❌ Error loading angel investors');
                }
            } catch (error) {
                console.error('❌ Angel investors error:', error);
                alert('❌ Network error loading angel investors');
            }
        },

        async loadAffiliatePartners(category = 'all') {
            try {
                console.log('🤝 Loading affiliate partners from:', `${API_BASE}/api/affiliate-partners?category=${category}`);
                const response = await fetch(`${API_BASE}/api/affiliate-partners?category=${category}`);
                console.log('📡 Response status:', response.status);
                const data = await response.json();
                console.log('📦 Data received:', data);
                
                if (data.success && data.partners) {
                    this.affiliatePartners = data.partners;
                    this.selectedAffiliateCategory = category;
                    console.log(`✅ Loaded ${data.partners.length} affiliate partners`);
                } else {
                    console.error('❌ Failed to load affiliate partners:', data);
                }
            } catch (error) {
                console.error('❌ Affiliate partners error:', error);
            }
        },

        togglePartnerContacted(partnerId) {
            if (this.contactedPartners.has(partnerId)) {
                this.contactedPartners.delete(partnerId);
            } else {
                this.contactedPartners.add(partnerId);
            }
            // Save to localStorage
            localStorage.setItem('contactedPartners', JSON.stringify([...this.contactedPartners]));
            console.log(`✅ Partner ${partnerId} contact status saved`);
        },

        isPartnerContacted(partnerId) {
            return this.contactedPartners.has(partnerId);
        },

        regenerateEmailVariant(partner) {
            // Cycle to next variant
            const currentVariant = this.partnerEmailVariants[partner.id] || 0;
            const nextVariant = (currentVariant + 1) % 5; // 5 templates per category
            this.partnerEmailVariants[partner.id] = nextVariant;
            localStorage.setItem('partnerEmailVariants', JSON.stringify(this.partnerEmailVariants));
            console.log(`🔄 Regenerated email for ${partner.name} - Variant ${nextVariant + 1}/5`);
        },

        generateOutreachMessage(partner) {
            const firstName = partner.name.split(' ')[0];
            const followers = partner.followers;
            const category = partner.category;
            
            // Get saved variant or use default (based on partner ID)
            const variantIndex = this.partnerEmailVariants[partner.id] !== undefined 
                ? this.partnerEmailVariants[partner.id] 
                : partner.id % 5;
            
            // Email-ready templates by category - longer with more context
            const templates = {
                audio: [
                    `Hey ${firstName}!\n\nI've been following your work and thought this might be perfect for your ${followers} community.\n\nWe built Zenyai - it's an AI tool that automatically organizes audio files using the most advanced metadata tagging. Think of it like having Google search, but for all your samples, loops, and project files.\n\nInstead of digging through folders for 20 minutes, you just type "find dark synth leads" or "808s from last month" and boom - it finds everything instantly. It reads your audio files and tags them automatically with tempo, key, mood, instrument type, everything.\n\nProducers tell us they're saving 5-10 hours per week just on finding files. Your audience deals with massive sample libraries - this would be a game-changer for them.\n\nWould love to explore a partnership. We could offer your community special early access.\n\nInterested in chatting?`,
                    
                    `${firstName},\n\nHuge fan of your tutorials! Quick question - how much time do you think your ${followers} followers spend hunting through sample folders?\n\nWe built Zenyai to solve exactly that problem. It's AI-powered file organization with smart metadata tagging that actually works.\n\nHere's what makes it different: You can search your audio files like you search Google. Type "trap hi-hats 150 BPM" and it finds every matching file across all your drives and folders. No manual tagging, no complicated setup - it just works.\n\nThe AI analyzes your audio and automatically tags everything - genre, mood, key, tempo, instrument type, even quality ratings. Producers are telling us it's like having a studio assistant who remembers where everything is.\n\nI think your community would absolutely love this. Would you be open to exploring a partnership? We're looking for creators who really get the organization struggle.\n\nLet me know!`,
                    
                    `Hey ${firstName}!\n\nYour content on production workflows really resonated with me. I bet your ${followers} audience deals with the same frustration we built Zenyai to solve.\n\nThe problem: You download hundreds of sample packs, save them in random folders, and 3 months later you can't find anything. Hours wasted digging instead of creating.\n\nOur solution: Zenyai uses AI to automatically read and tag all your audio files with advanced metadata. Then you just search in plain English - "show me bright piano loops" or "find vocal chops" - and it pulls up everything instantly.\n\nNo manual tagging. No organizing folders. Just search and create.\n\nWe've helped thousands of producers save hours every week. Your community would benefit massively from this, and I'd love to partner with you to get it in their hands.\n\nWant to explore working together?`,
                    
                    `${firstName}!\n\nI know you and your ${followers} followers work with huge sample libraries. Ever spent 30 minutes looking for "that one snare" you used last month?\n\nThat's exactly why we built Zenyai.\n\nIt's an AI that automatically organizes all your audio files using smart metadata tagging. You can search your entire music library like it's Spotify - just type what you're looking for in normal words and it finds it instantly.\n\nWhat makes it powerful: The AI actually listens to your files and tags them by sound, not just filename. So even if your file is called "audio_final_v3.wav", Zenyai knows it's a kick drum in C# at 128 BPM.\n\nProducers are telling us they've found samples they forgot they owned. It's like rediscovering your entire library.\n\nI think your audience needs this. Would you be interested in partnering with us? We could do special access for your community.\n\nLet's talk?`,
                    
                    `Hey ${firstName}!\n\nYour production content is incredible. I'm reaching out because I think Zenyai would solve a massive pain point for your ${followers} followers.\n\nHere's what it does: Zenyai automatically organizes audio files using AI-powered metadata tagging. But instead of complicated database stuff, you just search like you're talking to a person.\n\n"Find pluck sounds" - it finds them.\n"Show me all vocals in D minor" - there they are.\n"Loops from that Cymatics pack" - instant results.\n\nThe AI reads your files and tags them with everything - genre, key, tempo, mood, instrument, quality. It works across all your drives and folders automatically.\n\nWe're saving producers 5-10 hours per week. Your community would absolutely love this tool.\n\nWould you be open to exploring a partnership? I think we could create real value for your audience together.\n\nInterested?`
                ],
                film: [
                    `Hey ${firstName}!\n\nBig fan of your filmmaking content. I think Zenyai would be perfect for your ${followers} editor community.\n\nWe built it to solve the "where did I put that clip?" problem. It's AI-powered file organization with advanced metadata tagging, but for video files.\n\nHere's how it works: Instead of scrubbing through folders, you just search in plain English. "Find b-roll sunset shots" or "show me all drone footage from Italy" - and it finds everything instantly across all your drives.\n\nThe AI analyzes your video files and automatically tags them by content, location, shot type, color grade, everything. So even if your file is named "IMG_0042.mov", Zenyai knows it's a slow-motion beach shot at golden hour.\n\nEditors tell us they're saving 10+ hours per project just on finding footage. Your audience would absolutely benefit from this.\n\nWould love to explore a partnership. We could offer your community early access.\n\nInterested in chatting?`,
                    
                    `${firstName},\n\nYour editing tutorials are amazing! Quick question - how much time do your ${followers} followers spend searching for clips in their projects?\n\nWe built Zenyai to eliminate that problem entirely. It's AI that automatically organizes video files using smart metadata tagging.\n\nInstead of clicking through folders, you search like you're using Google: "Show me all interview clips" or "find that sunset b-roll" - and boom, instant results.\n\nWhat makes it powerful: The AI actually watches your videos and tags them by content. It recognizes faces, locations, shot types, movements, colors - everything. Then makes it all searchable in normal language.\n\nVideo editors are telling us they've cut their file-finding time by 80%. That's hours back every single project.\n\nI think your community needs this tool. Would you be open to partnering with us? We could create something special for your audience.\n\nLet me know!`,
                    
                    `Hey ${firstName}!\n\nI've been following your work and wanted to reach out about Zenyai. I think your ${followers} audience would absolutely love this.\n\nThe problem we solve: You shoot hundreds of clips, save them in folders, and when you need "that specific shot" weeks later, you can't find it. Hours wasted searching instead of editing.\n\nOur solution: Zenyai uses AI to automatically analyze and tag all your video files with advanced metadata. Then you just search in plain English - no complicated systems.\n\n"Find all establishing shots" - there they are.\n"Show me clips with cars" - instant results.\n"That interview about AI" - found it.\n\nIt works across all your drives and projects automatically. Editors are saving 5-10 hours per week just on file management.\n\nYour community would benefit massively. Want to explore a partnership?\n\nInterested?`,
                    
                    `${firstName}!\n\nYour content on video workflows is spot on. I bet your ${followers} followers deal with massive footage libraries too.\n\nThat's why we built Zenyai - AI-powered file organization that actually understands video content.\n\nHere's what makes it different: You can search your footage like it's YouTube. The AI watches your clips and tags them automatically - people, places, actions, shot types, everything.\n\nSo instead of opening 50 folders, you just type "beach drone shots" or "close-up reactions" and it finds everything instantly.\n\nFilmmakers tell us they're rediscovering footage they forgot they shot. It's like having a video assistant who remembers every single clip.\n\nI think your audience needs this. Would you be interested in partnering? We could offer your community special access.\n\nWant to chat about it?`,
                    
                    `Hey ${firstName}!\n\nLove what you're doing for the filmmaker community! I'm reaching out because Zenyai would solve a huge problem for your ${followers} editors.\n\nWe built an AI that organizes video files using advanced metadata tagging - but in a way that's actually easy to use.\n\nInstead of folder systems and manual organization, you just search naturally:\n\n"Find slow-motion water shots" - found.\n"Show all interviews from June" - there they are.\n"B-roll with golden hour lighting" - instant results.\n\nThe AI analyzes your video content and tags everything automatically. It recognizes what's actually in your clips, not just filenames.\n\nEditors are saving 10+ hours per project. Your community would absolutely benefit.\n\nWould you be open to partnering with us to bring this to your audience?\n\nLet's talk?`
                ],
                podcast: [
                    `Hey ${firstName}!\n\nHuge fan of your podcast! I think Zenyai would be perfect for your ${followers} listener community who also create content.\n\nWe built it to solve the podcast organization nightmare. It's AI-powered file management with smart metadata tagging specifically for audio content.\n\nHere's how it helps: Instead of digging through folders of episodes and clips, you just search naturally. "Find that quote about marketing" or "show all guest intros" - and it finds everything instantly.\n\nThe AI listens to your podcast files and automatically tags them with topics, speakers, themes, even key quotes. So you can search your entire podcast history like it's searchable transcripts.\n\nPodcasters tell us they're saving hours every week on prep and editing. Your audience would absolutely love this.\n\nWould you be interested in exploring a partnership? We could offer your listeners special access.\n\nWant to chat about it?`,
                    
                    `${firstName},\n\nYour podcast is incredible! Question - do your ${followers} listeners who podcast ever struggle finding specific clips or episodes?\n\nThat's exactly what Zenyai solves. It's AI that automatically organizes podcast files using advanced metadata tagging.\n\nInstead of listening back through hours of content, you just search: "Find when we talked about AI tools" or "show episode with Sarah" - boom, instant results.\n\nWhat makes it powerful: The AI actually listens to your content and understands it. It tags topics, speakers, themes, emotions, everything. Makes your entire podcast library searchable in normal language.\n\nPodcasters are telling us they're finding gold content they'd completely forgotten about. Perfect for creating clips, callbacks, and show prep.\n\nI think your community needs this. Would you be open to partnering with us?\n\nInterested in exploring this?`,
                    
                    `Hey ${firstName}!\n\nI've been listening to your show and wanted to reach out about Zenyai. Your ${followers} audience would benefit massively from this.\n\nThe problem: Podcasters record hundreds of hours of content, but finding specific moments later is nearly impossible. You waste hours searching for "that one quote" or "when we discussed X topic."\n\nOur solution: Zenyai uses AI to automatically analyze and tag all your podcast files with smart metadata. Then you search naturally:\n\n"Find all episodes about productivity" - found.\n"Show clips where I mentioned books" - there they are.\n"That story about the conference" - instant results.\n\nIt understands your content and makes everything searchable. Podcasters are saving 5+ hours per week on show prep and editing.\n\nYour community would love this tool. Want to explore a partnership?\n\nLet's chat?`,
                    
                    `${firstName}!\n\nYour podcast wisdom is amazing! I'm reaching out because your ${followers} listeners who create content deal with the exact problem Zenyai solves.\n\nWe built AI-powered organization for podcast files with advanced metadata tagging that actually works.\n\nHere's the magic: You can search your podcast library like it's Google. The AI listens to your content and tags it automatically - topics, guests, themes, key moments.\n\n"Find all marketing episodes" - boom.\n"Show interviews from Q2" - instant.\n"That quote about creativity" - found it.\n\nPodcasters tell us they're creating better content because they can actually reference their past work. It's like having a research assistant who's listened to every episode.\n\nI think your audience needs this. Would you be interested in partnering?\n\nWant to discuss?`,
                    
                    `Hey ${firstName}!\n\nLove your show! I'm reaching out because Zenyai would solve a massive pain point for your ${followers} podcaster community.\n\nWe built an AI that organizes podcast audio using smart metadata tagging - but in a way that's actually simple.\n\nInstead of complex systems, you just search naturally:\n\n"Find episode about social media" - there it is.\n"Show all guest interviews" - instant list.\n"That funny story about travel" - found immediately.\n\nThe AI analyzes your audio content and tags everything automatically. Topics, speakers, themes, emotions - all searchable.\n\nPodcasters are saving hours on show prep, editing, and creating social clips. Your community would absolutely benefit.\n\nWould you be open to partnering with us to bring this to your audience?\n\nInterested?`
                ],
                gaming: [
                    `Hey ${firstName}!\n\nLove your game dev content! I think Zenyai would be perfect for your ${followers} developer community.\n\nWe built it to solve the game asset organization problem. It's AI-powered file management with advanced metadata tagging for game projects.\n\nHere's how it works: Instead of hunting through project folders, you just search naturally. "Find character models" or "show UI elements" - and it finds everything instantly across all your projects.\n\nThe AI analyzes your game assets and automatically tags them by type, quality, usage, everything. Even if your file is named "final_v3_REAL.fbx", Zenyai knows it's a low-poly character model.\n\nGame devs tell us they're saving 10+ hours per week just on finding assets. Your audience would absolutely benefit from this.\n\nWould love to explore a partnership. We could offer your community early access.\n\nInterested in chatting?`,
                    
                    `${firstName},\n\nYour tutorials are amazing! Quick question - how much time do your ${followers} followers spend searching for assets in their game projects?\n\nWe built Zenyai to eliminate that entirely. It's AI that automatically organizes game files using smart metadata tagging.\n\nInstead of clicking through folders, you search like you're using Google: "Show me all weapon models" or "find explosion sounds" - boom, instant results.\n\nWhat makes it powerful: The AI understands game assets. It recognizes meshes, textures, sounds, animations - and tags them all automatically. Makes everything searchable in normal language.\n\nGame developers are telling us they've cut their asset-finding time by 80%. That's hours back every single project.\n\nI think your community needs this. Would you be open to partnering?\n\nLet me know!`,
                    
                    `Hey ${firstName}!\n\nI've been following your work and wanted to reach out about Zenyai. Your ${followers} audience would absolutely love this.\n\nThe problem: Game projects get messy fast. Hundreds of assets, multiple versions, scattered across folders. Finding that specific texture or sound effect becomes a nightmare.\n\nOur solution: Zenyai uses AI to automatically analyze and tag all your game files with smart metadata. Then you just search naturally:\n\n"Find all character textures" - there they are.\n"Show UI button assets" - instant results.\n"That jump sound effect" - found it.\n\nIt works across all your projects automatically. Devs are saving 5-10 hours per week on asset management.\n\nYour community would benefit massively. Want to explore a partnership?\n\nInterested?`,
                    
                    `${firstName}!\n\nYour game dev content is incredible! I bet your ${followers} followers deal with huge asset libraries too.\n\nThat's why we built Zenyai - AI-powered organization that actually understands game projects.\n\nHere's what makes it different: You can search your assets like it's the Unity Asset Store. The AI analyzes everything and tags it automatically - models, textures, sounds, scripts, animations.\n\nSo instead of opening 50 folders, you just type "environment props" or "enemy animation clips" and it finds everything instantly.\n\nGame devs tell us they're rediscovering assets they forgot they had. It's like having a technical artist who organizes everything.\n\nI think your audience needs this. Would you be interested in partnering?\n\nWant to chat?`,
                    
                    `Hey ${firstName}!\n\nLove what you're doing for the game dev community! I'm reaching out because Zenyai would solve a huge problem for your ${followers} developers.\n\nWe built an AI that organizes game assets using advanced metadata tagging - but in a way that's actually easy.\n\nInstead of folder systems and manual organization, you just search naturally:\n\n"Find low-poly character models" - found.\n"Show all texture files from last month" - there they are.\n"UI elements for inventory system" - instant results.\n\nThe AI analyzes your game content and tags everything automatically. It recognizes asset types, usage, quality - all searchable.\n\nDevelopers are saving 10+ hours per project. Your community would absolutely benefit.\n\nWould you be open to partnering with us?\n\nLet's talk?`
                ],
            };
            
            // Use the variant index
            const categoryTemplates = templates[category] || templates.audio;
            return categoryTemplates[variantIndex];
        },

        copyOutreachMessage(partner) {
            const message = this.generateOutreachMessage(partner);
            navigator.clipboard.writeText(message).then(() => {
                alert(`✅ Copied message for ${partner.name}!`);
            }).catch(err => {
                console.error('Failed to copy:', err);
            });
        },

        async sendEmailToPartner(partner) {
            const message = this.generateOutreachMessage(partner);
            const subject = `Partnership Opportunity with Zenyai`;
            
            try {
                const response = await fetch(`${API_BASE}/api/send-email`, {
                    method: 'POST',
                    headers: { 'Content-Type': 'application/json' },
                    body: JSON.stringify({
                        to: partner.email,
                        subject: subject,
                        body: message,
                        partner_name: partner.name
                    })
                });
                
                const data = await response.json();
                
                if (data.success) {
                    alert(`✅ Email sent to ${partner.name}!`);
                    // Automatically mark as contacted
                    this.contactedPartners.add(partner.name);
                    localStorage.setItem('contactedPartners', JSON.stringify([...this.contactedPartners]));
                } else {
                    alert(`❌ Failed to send email: ${data.error}`);
                }
            } catch (error) {
                console.error('Email send error:', error);
                alert(`❌ Error sending email. Make sure email settings are configured.`);
            }
        },

        async sendTestEmailToMyself(partner) {
            const message = this.generateOutreachMessage(partner);
            const subject = `[TEST] Partnership Opportunity with Zenyai - ${partner.name}`;
            const testEmail = prompt('Enter YOUR email address to receive test:', 'tomioladunjoye@zenyai.io');
            
            if (!testEmail) return;
            
            try {
                const response = await fetch(`${API_BASE}/api/send-email`, {
                    method: 'POST',
                    headers: { 'Content-Type': 'application/json' },
                    body: JSON.stringify({
                        to: testEmail,
                        subject: subject,
                        body: message,
                        partner_name: `TEST for ${partner.name}`
                    })
                });
                
                const data = await response.json();
                
                if (data.success) {
                    alert(`✅ Test email sent to ${testEmail}! Check your inbox.`);
                } else {
                    alert(`❌ Failed to send test email: ${data.error}`);
                }
            } catch (error) {
                console.error('Test email error:', error);
                alert(`❌ Error sending test email.`);
            }
        },

        // INVESTOR EMAIL FUNCTIONS
        toggleInvestorContacted(investorName) {
            if (this.contactedInvestors.has(investorName)) {
                this.contactedInvestors.delete(investorName);
            } else {
                this.contactedInvestors.add(investorName);
            }
            localStorage.setItem('contactedInvestors', JSON.stringify([...this.contactedInvestors]));
            console.log(`✅ Investor ${investorName} contact status saved`);
        },

        isInvestorContacted(investorName) {
            return this.contactedInvestors.has(investorName);
        },

        regenerateInvestorEmail(investor) {
            const currentVariant = this.investorEmailVariants[investor.name] || 0;
            const nextVariant = (currentVariant + 1) % 5;
            this.investorEmailVariants[investor.name] = nextVariant;
            localStorage.setItem('investorEmailVariants', JSON.stringify(this.investorEmailVariants));
            console.log(`🔄 Regenerated email for ${investor.name} - Variant ${nextVariant + 1}/5`);
        },

        generateInvestorPitch(investor) {
            const firstName = investor.name.split(' ')[0];
            
            // Generate personalized admiration line based on their actual accomplishments
            const getAdmirationLine = (investor) => {
                const name = investor.name.toLowerCase();
                
                // Tech Industry Leaders
                if (name.includes('drew houston')) return `I admire how you built Dropbox from a simple idea to serve 700M+ users globally`;
                if (name.includes('aaron levie')) return `I admire how you built Box into a $3B+ enterprise file management leader`;
                if (name.includes('dylan field')) return `I admire how you built Figma into the $20B design tool that revolutionized creative collaboration`;
                if (name.includes('stewart butterfield')) return `I admire how you built Slack into the $27B workplace communication platform`;
                if (name.includes('dustin moskovitz')) return `I admire how you co-founded Facebook and built Asana to solve workflow problems for millions`;
                if (name.includes('patrick collison')) return `I admire how you built Stripe into the $95B payments infrastructure powering the internet`;
                if (name.includes('john collison')) return `I admire how you co-built Stripe to become the backbone of online commerce`;
                if (name.includes('reid hoffman')) return `I admire how you built LinkedIn into the world's largest professional network`;
                if (name.includes('tobias')) return `I admire how you built Shopify to empower millions of entrepreneurs globally`;
                if (name.includes('mark cuban')) return `I admire your track record of backing game-changing companies like Dropbox and Twitter`;
                if (name.includes('eric schmidt')) return `I admire your leadership at Google and your continued investment in transformative AI companies`;
                
                // Music/Audio Industry Leaders  
                if (name.includes('michael mignano')) return `I admire how you built Anchor and sold it to Spotify for $340M, revolutionizing podcasting`;
                if (name.includes('eric wahlforss')) return `I admire how you co-founded SoundCloud and built the largest audio sharing platform for creators`;
                if (name.includes('steve martocci')) return `I admire how you built Splice into the leading music production platform serving millions of producers`;
                if (name.includes('alexander ljung')) return `I admire how you co-founded SoundCloud and created the platform that launched countless music careers`;
                if (name.includes('nir zicherman')) return `I admire how you co-built Anchor and now lead audio innovation at Spotify`;
                if (name.includes('jimmy iovine')) return `I admire your legendary career building Interscope Records and co-founding Beats`;
                if (name.includes('troy carter')) return `I admire how you managed Lady Gaga's career and now invest in creator economy companies`;
                
                // Creator Economy Experts
                if (name.includes('li jin')) return `I admire how you coined "creator economy" and built Atelier to back creator-focused startups`;
                if (name.includes('andrew chen')) return `I admire your expertise in network effects and your investments in creator platforms at a16z`;
                if (name.includes('packy mccormick')) return `I admire how you built Not Boring into a media empire and became a creator-investor`;
                if (name.includes('david perell')) return `I admire how you built Write of Passage and became the leading educator for online creators`;
                if (name.includes('tiago forte')) return `I admire how you built Building a Second Brain and revolutionized productivity for creators`;
                
                // AI/ML Specialists
                if (name.includes('andrej karpathy')) return `I admire your pioneering work in AI at Tesla and OpenAI, advancing computer vision`;
                if (name.includes('andrew ng')) return `I admire how you democratized AI education through Coursera and built Google Brain`;
                if (name.includes('pieter abbeel')) return `I admire your groundbreaking robotics AI research at UC Berkeley and Covariant`;
                if (name.includes('fei-fei li')) return `I admire your computer vision pioneering work at Stanford and leadership in AI ethics`;
                if (name.includes('daphne koller')) return `I admire how you co-founded Coursera and now apply ML to drug discovery at insitro`;
                if (name.includes('sam altman')) return `I admire your leadership at OpenAI, bringing AI to mainstream adoption`;
                if (name.includes('ilya sutskever')) return `I admire your foundational work in deep learning and co-founding OpenAI`;
                
                // Additional investors
                if (name.includes('hiten shah')) return `I admire how you built multiple successful SaaS companies like Crazy Egg and FYI`;
                if (name.includes('dharmesh shah')) return `I admire how you co-built HubSpot into a $30B+ marketing platform`;
                if (name.includes('josh elman')) return `I admire your product leadership at Twitter and LinkedIn, and your investments at Greylock`;
                if (name.includes('sarah tavel')) return `I admire your marketplace expertise at Pinterest and your investments at Benchmark`;
                
                // Default for any investor not specifically mapped
                return `I admire your track record of backing innovative companies that solve real problems`;
            };
            
            const admirationLine = getAdmirationLine(investor);
            
            const variantIndex = this.investorEmailVariants[investor.name] !== undefined 
                ? this.investorEmailVariants[investor.name] 
                : Math.abs(investor.name.split('').reduce((a,b)=>a+b.charCodeAt(0),0)) % 5;
            
            const templates = [
                `${firstName},\n\n${admirationLine}, and I'm solving the number one pain with audio professionals and there's a huge market opportunity.\n\nI'm an Oscar qualified film composer and I developed an AI that helps audio professionals store and auto tag their sounds where they're able to talk to their storage with natural language. We aim to be the go-to audio storage manager platform and there's a $2 billion market opportunity.\n\nWould you like to see a demo or jump on a call? Let me know.\n\nTomi from zenyai.io`,

                `Hi ${firstName},\n\n${admirationLine}, and I'm solving the number one pain with audio professionals and there's a huge market opportunity.\n\nI'm an Oscar qualified film composer and I developed an AI that helps audio professionals store and auto tag their sounds where they're able to talk to their storage with natural language. We aim to be the go-to audio storage manager platform and there's a $2 billion market opportunity.\n\nWould you like to see a demo or jump on a call? Let me know.\n\nTomi from zenyai.io`,

                `${firstName},\n\n${admirationLine}, and I'm solving the number one pain with audio professionals and there's a huge market opportunity.\n\nI'm an Oscar qualified film composer and I developed an AI that helps audio professionals store and auto tag their sounds where they're able to talk to their storage with natural language. We aim to be the go-to audio storage manager platform and there's a $2 billion market opportunity.\n\nWould you like to see a demo or jump on a call? Let me know.\n\nTomi from zenyai.io`,

                `Hi ${firstName},\n\n${admirationLine}, and I'm solving the number one pain with audio professionals and there's a huge market opportunity.\n\nI'm an Oscar qualified film composer and I developed an AI that helps audio professionals store and auto tag their sounds where they're able to talk to their storage with natural language. We aim to be the go-to audio storage manager platform and there's a $2 billion market opportunity.\n\nWould you like to see a demo or jump on a call? Let me know.\n\nTomi from zenyai.io`,

                `${firstName},\n\n${admirationLine}, and I'm solving the number one pain with audio professionals and there's a huge market opportunity.\n\nI'm an Oscar qualified film composer and I developed an AI that helps audio professionals store and auto tag their sounds where they're able to talk to their storage with natural language. We aim to be the go-to audio storage manager platform and there's a $2 billion market opportunity.\n\nWould you like to see a demo or jump on a call? Let me know.\n\nTomi from zenyai.io`
            ];
            
            return templates[variantIndex];
        },

        copyInvestorPitch(investor) {
            const message = this.generateInvestorPitch(investor);
            navigator.clipboard.writeText(message).then(() => {
                alert(`✅ Copied investment pitch for ${investor.name}!`);
            }).catch(err => {
                console.error('Failed to copy:', err);
            });
        },

        async sendEmailToInvestor(investor) {
            const message = this.generateInvestorPitch(investor);
            const subject = `Zenyai Pre-Seed: AI File Organization for Creators`;
            
            try {
                const response = await fetch(`${API_BASE}/api/send-email`, {
                    method: 'POST',
                    headers: { 'Content-Type': 'application/json' },
                    body: JSON.stringify({
                        to: investor.email,
                        subject: subject,
                        body: message,
                        partner_name: investor.name
                    })
                });
                
                const data = await response.json();
                
                if (data.success) {
                    alert(`✅ Email sent to ${investor.name}!`);
                    this.contactedInvestors.add(investor.name);
                    localStorage.setItem('contactedInvestors', JSON.stringify([...this.contactedInvestors]));
                } else {
                    alert(`❌ Failed to send email: ${data.error}`);
                }
            } catch (error) {
                console.error('Email send error:', error);
                alert(`❌ Error sending email. Make sure email settings are configured.`);
            }
        },

        async sendTestInvestorEmail(investor) {
            const message = this.generateInvestorPitch(investor);
            const subject = `[TEST] Zenyai Pre-Seed Investment - ${investor.name}`;
            const testEmail = prompt('Enter YOUR email address to receive test:', 'tomioladunjoye@zenyai.io');
            
            if (!testEmail) return;
            
            try {
                const response = await fetch(`${API_BASE}/api/send-email`, {
                    method: 'POST',
                    headers: { 'Content-Type': 'application/json' },
                    body: JSON.stringify({
                        to: testEmail,
                        subject: subject,
                        body: message,
                        partner_name: `TEST for ${investor.name}`
                    })
                });
                
                const data = await response.json();
                
                if (data.success) {
                    alert(`✅ Test email sent to ${testEmail}! Check your inbox.`);
                } else {
                    alert(`❌ Failed to send test email: ${data.error}`);
                }
            } catch (error) {
                console.error('Test email error:', error);
                alert(`❌ Error sending test email.`);
            }
        },

        // BULK SEND FUNCTIONS
        async bulkSendInvestorEmails() {
            // TRIPLE CHECK: Filter for uncontacted investors only
            // Convert object to array if needed
            const investorsArray = Array.isArray(this.angelInvestors) 
                ? this.angelInvestors 
                : Object.values(this.angelInvestors || {});
            const uncontactedInvestors = investorsArray.filter(inv => !this.isInvestorContacted(inv.name));
            
            if (uncontactedInvestors.length === 0) {
                alert('📧 All investors have been contacted!\n\nNo duplicate emails will be sent.');
                return;
            }
            
            const batchSize = 12;
            const batch = uncontactedInvestors.slice(0, batchSize);
            
            // Show detailed confirmation with contacted status
            const contactedCount = investorsArray.length - uncontactedInvestors.length;
            const confirmMessage = `📧 BULK SEND CONFIRMATION:\n\n` +
                `✅ Already contacted: ${contactedCount} investors\n` +
                `📧 Will send to: ${batch.length} NEW investors (UNCONTACTED ONLY)\n` +
                `⏳ Remaining after this batch: ${uncontactedInvestors.length - batch.length}\n\n` +
                `NEXT 12 UNCONTACTED RECIPIENTS:\n${batch.map(inv => `• ${inv.name} ✉️`).join('\n')}\n\n` +
                `Continue with bulk send to UNCONTACTED investors only?`;
                
            const confirmed = confirm(confirmMessage);
            if (!confirmed) return;
            
            let successCount = 0;
            let failCount = 0;
            let duplicateSkipped = 0;
            
            for (const investor of batch) {
                try {
                    // SAFETY CHECK: Double-check not already contacted before sending
                    if (this.isInvestorContacted(investor.name)) {
                        console.log(`⚠️ DUPLICATE PREVENTED: ${investor.name} already contacted, skipping`);
                        duplicateSkipped++;
                        continue;
                    }
                    
                    const message = this.generateInvestorPitch(investor);
                    const subject = `Zenyai: AI Audio File Management Solution`;
                    
                    console.log(`📧 Sending to ${investor.name} (${investor.email})`);
                    
                    const response = await fetch(`${API_BASE}/api/send-email`, {
                        method: 'POST',
                        headers: { 'Content-Type': 'application/json' },
                        body: JSON.stringify({
                            to: investor.email,
                            subject: subject,
                            body: message,
                            partner_name: investor.name
                        })
                    });
                    
                    const data = await response.json();
                    
                    if (data.success) {
                        // IMMEDIATELY mark as contacted to prevent duplicates
                        this.toggleInvestorContacted(investor.name);
                        successCount++;
                        console.log(`✅ SENT & MARKED: ${investor.name} - Email sent and marked as contacted`);
                    } else {
                        failCount++;
                        console.error(`❌ Failed to send to ${investor.name}: ${data.error}`);
                    }
                    
                    // Delay between emails to prevent rate limiting
                    await new Promise(resolve => setTimeout(resolve, 1000));
                    
                } catch (error) {
                    failCount++;
                    console.error(`❌ Error sending to ${investor.name}:`, error);
                }
            }
            
            const finalInvestorsArray = Array.isArray(this.angelInvestors) 
                ? this.angelInvestors 
                : Object.values(this.angelInvestors || {});
            const remainingCount = finalInvestorsArray.filter(inv => !this.isInvestorContacted(inv.name)).length;
            
            alert(`📊 BULK SEND COMPLETE!\n\n` +
                `✅ Successfully sent: ${successCount}\n` +
                `❌ Failed to send: ${failCount}\n` +
                `⚠️ Duplicates prevented: ${duplicateSkipped}\n` +
                `📧 Remaining uncontacted: ${remainingCount} investors\n\n` +
                `All sent emails are permanently marked as contacted to prevent duplicates.`);
        },

        async bulkSendPartnerEmails() {
            // TRIPLE CHECK: Filter for uncontacted partners only
            const uncontactedPartners = this.affiliatePartners.filter(partner => !this.isPartnerContacted(partner.name));
            
            if (uncontactedPartners.length === 0) {
                alert('📧 All partners have been contacted!\n\nNo duplicate emails will be sent.');
                return;
            }
            
            const batchSize = 12;
            const batch = uncontactedPartners.slice(0, batchSize);
            
            // Show detailed confirmation with contacted status
            const contactedCount = this.affiliatePartners.length - uncontactedPartners.length;
            const confirmMessage = `📧 BULK SEND CONFIRMATION:\n\n` +
                `✅ Already contacted: ${contactedCount} partners\n` +
                `📧 Will send to: ${batch.length} NEW partners (UNCONTACTED ONLY)\n` +
                `⏳ Remaining after this batch: ${uncontactedPartners.length - batch.length}\n\n` +
                `NEXT 12 UNCONTACTED RECIPIENTS:\n${batch.map(p => `• ${p.name} ✉️`).join('\n')}\n\n` +
                `Continue with bulk send to UNCONTACTED partners only?`;
                
            const confirmed = confirm(confirmMessage);
            if (!confirmed) return;
            
            let successCount = 0;
            let failCount = 0;
            let duplicateSkipped = 0;
            
            for (const partner of batch) {
                try {
                    // SAFETY CHECK: Double-check not already contacted before sending
                    if (this.isPartnerContacted(partner.name)) {
                        console.log(`⚠️ DUPLICATE PREVENTED: ${partner.name} already contacted, skipping`);
                        duplicateSkipped++;
                        continue;
                    }
                    
                    const message = this.generateOutreachMessage(partner);
                    const subject = `Partnership Opportunity with Zenyai - ${partner.name}`;
                    
                    console.log(`📧 Sending to ${partner.name} (${partner.email})`);
                    
                    const response = await fetch(`${API_BASE}/api/send-email`, {
                        method: 'POST',
                        headers: { 'Content-Type': 'application/json' },
                        body: JSON.stringify({
                            to: partner.email,
                            subject: subject,
                            body: message,
                            partner_name: partner.name
                        })
                    });
                    
                    const data = await response.json();
                    
                    if (data.success) {
                        // IMMEDIATELY mark as contacted to prevent duplicates
                        this.togglePartnerContacted(partner.name);
                        successCount++;
                        console.log(`✅ SENT & MARKED: ${partner.name} - Email sent and marked as contacted`);
                    } else {
                        failCount++;
                        console.error(`❌ Failed to send to ${partner.name}: ${data.error}`);
                    }
                    
                    // Delay between emails to prevent rate limiting
                    await new Promise(resolve => setTimeout(resolve, 1000));
                    
                } catch (error) {
                    failCount++;
                    console.error(`❌ Error sending to ${partner.name}:`, error);
                }
            }
            
            const remainingCount = this.affiliatePartners.filter(partner => !this.isPartnerContacted(partner.name)).length;
            
            alert(`📊 BULK SEND COMPLETE!\n\n` +
                `✅ Successfully sent: ${successCount}\n` +
                `❌ Failed to send: ${failCount}\n` +
                `⚠️ Duplicates prevented: ${duplicateSkipped}\n` +
                `📧 Remaining uncontacted: ${remainingCount} partners\n\n` +
                `All sent emails are permanently marked as contacted to prevent duplicates.`);
        },

        // DEBUG FUNCTION - Check memory status
        debugMemoryStatus() {
            const contactedPartners = JSON.parse(localStorage.getItem('contactedPartners') || '[]');
            const contactedInvestors = JSON.parse(localStorage.getItem('contactedInvestors') || '[]');
            
            console.log('🔍 MEMORY DEBUG:');
            console.log('📧 Contacted Partners:', contactedPartners);
            console.log('💰 Contacted Investors:', contactedInvestors);
            console.log('🔢 Partner Count:', contactedPartners.length);
            console.log('🔢 Investor Count:', contactedInvestors.length);
            
            alert(`🔍 MEMORY STATUS:\n\n` +
                `📧 Contacted Partners: ${contactedPartners.length}\n` +
                `Partners: ${contactedPartners.join(', ')}\n\n` +
                `💰 Contacted Investors: ${contactedInvestors.length}\n` +
                `Investors: ${contactedInvestors.join(', ')}\n\n` +
                `Check console for full details.`);
        },

        // CLEAR MEMORY FUNCTION - For testing
        clearAllMemory() {
            if (confirm('⚠️ CLEAR ALL MEMORY?\n\nThis will reset all contacted status. Continue?')) {
                localStorage.removeItem('contactedPartners');
                localStorage.removeItem('contactedInvestors');
                localStorage.removeItem('partnerEmailVariants');
                localStorage.removeItem('investorEmailVariants');
                
                this.contactedPartners = new Set();
                this.contactedInvestors = new Set();
                this.partnerEmailVariants = {};
                this.investorEmailVariants = {};
                
                alert('🗑️ All memory cleared! Refresh page to see changes.');
            }
        },

        async loadCompetitorOverview() {
            try {
                console.log('🔍 Loading competitor overview...');
                const response = await fetch(`${API_BASE}/api/competitors/overview`);
                const data = await response.json();
                
                if (data.success) {
                    this.competitorOverview = data.overview;
                    console.log(`✅ Loaded ${data.overview.total_competitors} competitors`);
                } else {
                    console.error('❌ Failed to load competitors:', data.error);
                }
            } catch (error) {
                console.error('❌ Competitor overview error:', error);
            }
        },

        async loadCompetitorRankings() {
            try {
                console.log('📊 Loading competitor rankings...');
                this.loadingCompetitors = true;
                const response = await fetch(`${API_BASE}/api/competitors/rankings`);
                const data = await response.json();
                
                if (data.success) {
                    this.competitorRankings = data.rankings;
                    console.log(`✅ Ranked ${data.rankings.length} competitors`);
                } else {
                    console.error('❌ Failed to load rankings:', data.error);
                }
            } catch (error) {
                console.error('❌ Competitor rankings error:', error);
            } finally {
                this.loadingCompetitors = false;
            }
        },

        async analyzeCompetitor(competitorKey) {
            try {
                console.log(`🔍 Analyzing ${competitorKey}...`);
                this.loadingCompetitors = true;
                this.selectedCompetitor = competitorKey;
                
                const response = await fetch(`${API_BASE}/api/competitors/analyze/${competitorKey}`);
                const data = await response.json();
                
                if (data.success) {
                    this.competitorAnalysis = data.analysis;
                    console.log(`✅ Analysis complete for ${data.analysis.competitor}`);
                } else {
                    console.error('❌ Failed to analyze competitor:', data.error);
                }
            } catch (error) {
                console.error('❌ Competitor analysis error:', error);
            } finally {
                this.loadingCompetitors = false;
            }
        },

        async batchAnalyzeCompetitors() {
            try {
                console.log('🔍 Running batch competitor analysis...');
                this.loadingCompetitors = true;
                
                const response = await fetch(`${API_BASE}/api/competitors/batch-analyze`, {
                    method: 'POST',
                    headers: { 'Content-Type': 'application/json' },
                    body: JSON.stringify({
                        competitors: ['descript', 'riverside', 'splice', 'landr', 'otter']
                    })
                });
                const data = await response.json();
                
                if (data.success) {
                    console.log(`✅ Batch analysis complete: ${data.analyzed_count} competitors`);
                    // Refresh rankings with new data
                    await this.loadCompetitorRankings();
                    alert(`✅ Analyzed ${data.analyzed_count} competitors!`);
                } else {
                    console.error('❌ Batch analysis failed:', data.error);
                }
            } catch (error) {
                console.error('❌ Batch analysis error:', error);
                alert('❌ Error running batch analysis');
            } finally {
                this.loadingCompetitors = false;
            }
        },

        async runComprehensiveAnalysis() {
            this.analysisRunning = true;
            
            try {
                const response = await fetch(`${API_BASE}/api/run-comprehensive-analysis`, {
                    method: 'POST',
                    headers: { 'Content-Type': 'application/json' }
                });
                const data = await response.json();
                
                if (data.success) {
                    const summary = data.data.analysis_summary;
                    const tamSamSom = data.data.market_analysis.tam_sam_som;
                    
                    this.tamValue = tamSamSom.tam.value;
                    this.samValue = tamSamSom.sam.value;
                    this.somValue = tamSamSom.som.value;
                    this.overallConfidence = Math.round(summary.overall_confidence);
                    this.totalCompetitors = summary.total_competitors;
                    this.dataConfidence = this.overallConfidence;
                    
                    alert(`🎉 Analysis Complete! ${summary.total_competitors} competitors analyzed`);
                }
            } catch (err) {
                alert('❌ Network error: ' + err.message);
            } finally {
                this.analysisRunning = false;
            }
        }
    }
}

// Dashboard HTML
const dashboardHTML = `
<div class="flex h-screen bg-gray-900" x-data="intelligenceDashboard()">
    <!-- Sidebar -->
    <div class="w-64 card-dark border-r border-gray-700">
        <div class="p-6 border-b border-gray-700">
            <div class="flex items-center space-x-3">
                <div class="w-10 h-10 bg-gradient-to-r from-purple-600 to-blue-600 rounded-lg flex items-center justify-center">
                    <i class="fas fa-brain text-white"></i>
                </div>
                <div>
                    <h1 class="text-lg font-bold">Zenyai</h1>
                    <p class="text-xs text-gray-400">Intelligence Platform</p>
                </div>
            </div>
        </div>

        <nav class="p-4 space-y-2">
            <a href="#" @click="switchView('dashboard')" 
               :class="currentView === 'dashboard' ? 'bg-blue-600' : 'hover:bg-gray-700'"
               class="flex items-center space-x-3 px-4 py-3 rounded-lg transition-colors">
                <i class="fas fa-chart-line w-5"></i>
                <span>Dashboard</span>
            </a>
            <a href="#" @click="switchView('competitors')" 
               :class="currentView === 'competitors' ? 'bg-blue-600' : 'hover:bg-gray-700'"
               class="flex items-center space-x-3 px-4 py-3 rounded-lg transition-colors">
                <i class="fas fa-users w-5"></i>
                <span>Competitors</span>
            </a>
            <a href="#" @click="switchView('pain-points')" 
               :class="currentView === 'pain-points' ? 'bg-blue-600' : 'hover:bg-gray-700'"
               class="flex items-center space-x-3 px-4 py-3 rounded-lg transition-colors">
                <i class="fas fa-exclamation-triangle w-5"></i>
                <span>Pain Points</span>
            </a>
            <a href="#" @click="switchView('social-intel')" 
               :class="currentView === 'social-intel' ? 'bg-blue-600' : 'hover:bg-gray-700'"
               class="flex items-center space-x-3 px-4 py-3 rounded-lg transition-colors">
                <i class="fas fa-share-alt w-5"></i>
                <span>Social Intel</span>
            </a>
            <a href="#" @click="switchView('financial')" 
               :class="currentView === 'financial' ? 'bg-blue-600' : 'hover:bg-gray-700'"
               class="flex items-center space-x-3 px-4 py-3 rounded-lg transition-colors">
                <i class="fas fa-dollar-sign w-5"></i>
                <span>Financial</span>
            </a>
            <a href="#" @click="switchView('marketing-videos')" 
               :class="currentView === 'marketing-videos' ? 'bg-blue-600' : 'hover:bg-gray-700'"
               class="flex items-center space-x-3 px-4 py-3 rounded-lg transition-colors">
                <i class="fas fa-video w-5"></i>
                <span>Marketing Videos</span>
            </a>
            
            <a href="#" @click="switchView('audio-intelligence')" 
               :class="currentView === 'audio-intelligence' ? 'bg-blue-600' : 'hover:bg-gray-700'"
               class="flex items-center space-x-3 px-4 py-3 rounded-lg transition-colors">
                <i class="fas fa-headphones w-5"></i>
                <span>Audio Intelligence</span>
            </a>
            
            <a href="#" @click="switchView('angel-investors')" 
               :class="currentView === 'angel-investors' ? 'bg-blue-600' : 'hover:bg-gray-700'"
               class="flex items-center space-x-3 px-4 py-3 rounded-lg transition-colors">
                <i class="fas fa-hand-holding-usd w-5"></i>
                <span>Angel Investors</span>
            </a>
            <a href="#" @click="switchView('affiliate-partners')" 
               :class="currentView === 'affiliate-partners' ? 'bg-blue-600' : 'hover:bg-gray-700'"
               class="flex items-center space-x-3 px-4 py-3 rounded-lg transition-colors">
                <i class="fas fa-handshake w-5"></i>
                <span>Affiliate Partners</span>
            </a>
        </nav>
    </div>

    <!-- Main Content -->
    <div class="flex-1 flex flex-col">
        <!-- Header -->
        <header class="card-dark border-b border-gray-700 px-6 py-4">
            <div class="flex items-center justify-between">
                <div>
                    <h2 class="text-xl font-bold" x-text="getViewTitle()">Dashboard</h2>
                    <p class="text-sm text-gray-400">Real-time market intelligence and analytics</p>
                </div>
                <div class="flex items-center space-x-4">
                    <div class="flex items-center space-x-2">
                        <div class="w-2 h-2 bg-green-500 rounded-full"></div>
                        <span class="text-sm text-gray-400">Live Data</span>
                    </div>
                </div>
            </div>
        </header>

        <!-- Dashboard Content -->
        <div class="p-6 h-full overflow-y-auto">
            <!-- Dashboard View -->
            <div x-show="currentView === 'dashboard'" class="space-y-6">
                <!-- RUN ANALYSIS Button -->
                <div class="card-dark rounded-xl p-6">
                    <div class="flex items-center justify-between">
                        <div>
                            <h3 class="text-xl font-bold text-white mb-2">Market Intelligence Dashboard</h3>
                            <p class="text-lg text-blue-400 font-semibold" x-text="currentIdea"></p>
                        </div>
                        <button @click="runComprehensiveAnalysis()" 
                                :disabled="analysisRunning"
                                class="bg-gradient-to-r from-red-600 to-orange-600 hover:from-red-700 hover:to-orange-700 text-white font-bold py-3 px-6 rounded-lg transition-all disabled:opacity-50">
                            <i class="fas fa-rocket mr-2" :class="analysisRunning ? 'fa-spin fa-spinner' : 'fa-rocket'"></i>
                            <span x-text="analysisRunning ? 'ANALYZING...' : 'RUN ANALYSIS'"></span>
                        </button>
                    </div>
                </div>

                <!-- Business Thesis / North Star -->
                <div class="card-dark rounded-xl p-6 border border-blue-500/30">
                    <div class="flex items-start gap-4">
                        <div class="bg-blue-600/20 rounded-full p-3">
                            <i class="fas fa-star text-blue-400 text-xl"></i>
                        </div>
                        <div class="flex-1">
                            <h3 class="text-lg font-bold text-blue-400 mb-2">Business Thesis & North Star</h3>
                            <div class="grid grid-cols-1 lg:grid-cols-2 gap-6">
                                <div>
                                    <h4 class="font-semibold mb-3">🎯 Core Thesis</h4>
                                    <p class="text-sm text-gray-300 mb-4">
                                        <strong>Audio professionals experience the highest metadata organization pain (92.0/100) of all creative professions.</strong> 
                                        With 487K professionals willing to pay $125/month and a $1.84B TAM, Zenyai targets the most painful creative workflow problem with AI-first organization.
                                    </p>
                                    <div class="space-y-2">
                                        <div class="flex items-center gap-2">
                                            <i class="fas fa-check-circle text-green-400 text-sm"></i>
                                            <span class="text-xs">Highest pain score across 14 creative professions</span>
                                        </div>
                                        <div class="flex items-center gap-2">
                                            <i class="fas fa-check-circle text-green-400 text-sm"></i>
                                            <span class="text-xs">Research-first approach validates every pain point</span>
                                        </div>
                                        <div class="flex items-center gap-2">
                                            <i class="fas fa-check-circle text-green-400 text-sm"></i>
                                            <span class="text-xs">AI-powered solution with dramatic visual metaphors</span>
                                        </div>
                                    </div>
                                </div>
                                <div>
                                    <h4 class="font-semibold mb-3">🌟 North Star Vision</h4>
                                    <p class="text-sm text-gray-300 mb-4">
                                        <strong>"Make creative chaos extinct through intelligent AI organization."</strong> 
                                        Transform the most painful creative workflow into the most satisfying, starting with audio professionals and expanding to all creative metadata.
                                    </p>
                                    <div class="grid grid-cols-2 gap-3">
                                        <div class="bg-gray-800/50 rounded p-3 text-center">
                                            <p class="text-lg font-bold text-purple-400">$108M</p>
                                            <p class="text-xs text-gray-400">Year 5 Revenue (Aggressive)</p>
                                        </div>
                                        <div class="bg-gray-800/50 rounded p-3 text-center">
                                            <p class="text-lg font-bold text-blue-400">403K</p>
                                            <p class="text-xs text-gray-400">Year 5 Users</p>
                                        </div>
                                        <div class="bg-gray-800/50 rounded p-3 text-center">
                                            <p class="text-lg font-bold text-green-400">92.0</p>
                                            <p class="text-xs text-gray-400">Pain Score (Audio)</p>
                                        </div>
                                        <div class="bg-gray-800/50 rounded p-3 text-center">
                                            <p class="text-lg font-bold text-orange-400">18.5:1</p>
                                            <p class="text-xs text-gray-400">LTV:CAC Ratio</p>
                                        </div>
                                    </div>
                                </div>
                            </div>
                        </div>
                    </div>
                </div>

                <!-- Key Metrics Row 1: TAM/SAM/SOM + Confidence -->
                <div class="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-5 gap-4">
                    <div class="metric-card rounded-xl p-4">
                        <div class="flex items-center justify-between">
                            <div>
                                <p class="text-gray-400 text-xs">TAM (Total Addressable)</p>
                                <p class="text-xl font-bold" x-text="formatCurrency(tamValue)">$1.84B</p>
                                <p class="text-blue-500 text-xs flex items-center mt-1">
                                    <i class="fas fa-globe mr-1"></i>
                                    <span x-text="tamConfidence + '% confidence'">89% confidence</span>
                                </p>
                            </div>
                            <div class="w-10 h-10 bg-blue-500/20 rounded-lg flex items-center justify-center">
                                <i class="fas fa-globe text-blue-400 text-sm"></i>
                            </div>
                        </div>
                    </div>
                    <div class="metric-card rounded-xl p-4">
                        <div class="flex items-center justify-between">
                            <div>
                                <p class="text-gray-400 text-xs">SAM (Serviceable)</p>
                                <p class="text-xl font-bold" x-text="formatCurrency(samValue)">$772M</p>
                                <p class="text-purple-500 text-xs flex items-center mt-1">
                                    <i class="fas fa-target mr-1"></i>
                                    <span x-text="samConfidence + '% confidence'">84% confidence</span>
                                </p>
                            </div>
                            <div class="w-10 h-10 bg-purple-500/20 rounded-lg flex items-center justify-center">
                                <i class="fas fa-target text-purple-400 text-sm"></i>
                            </div>
                        </div>
                    </div>
                    <div class="metric-card rounded-xl p-4">
                        <div class="flex items-center justify-between">
                            <div>
                                <p class="text-gray-400 text-xs">SOM (Obtainable)</p>
                                <p class="text-xl font-bold" x-text="formatCurrency(somValue)">$11.6M</p>
                                <p class="text-green-500 text-xs flex items-center mt-1">
                                    <i class="fas fa-bullseye mr-1"></i>
                                    <span x-text="somConfidence + '% confidence'">76% confidence</span>
                                </p>
                            </div>
                            <div class="w-10 h-10 bg-green-500/20 rounded-lg flex items-center justify-center">
                                <i class="fas fa-bullseye text-green-400 text-sm"></i>
                            </div>
                        </div>
                    </div>
                    <div class="metric-card rounded-xl p-4">
                        <div class="flex items-center justify-between">
                            <div>
                                <p class="text-gray-400 text-xs">Competitors Analyzed</p>
                                <p class="text-xl font-bold" x-text="totalCompetitors">30</p>
                                <p class="text-orange-500 text-xs flex items-center mt-1">
                                    <i class="fas fa-users mr-1"></i>
                                    <span x-text="'Top threat: ' + topThreat">Splice (95)</span>
                                </p>
                            </div>
                            <div class="w-10 h-10 bg-orange-500/20 rounded-lg flex items-center justify-center">
                                <i class="fas fa-users text-orange-400 text-sm"></i>
                            </div>
                        </div>
                    </div>
                    <div class="metric-card rounded-xl p-4">
                        <div class="flex items-center justify-between">
                            <div>
                                <p class="text-gray-400 text-xs">Analysis Confidence</p>
                                <p class="text-xl font-bold" x-text="overallConfidence + '%'">86%</p>
                                <p class="text-green-500 text-xs flex items-center mt-1">
                                    <i class="fas fa-check-circle mr-1"></i>
                                    <span x-text="getConfidenceLevel(overallConfidence)">High Accuracy</span>
                                </p>
                            </div>
                            <div class="w-10 h-10 bg-green-500/20 rounded-lg flex items-center justify-center">
                                <i class="fas fa-check-circle text-green-400 text-sm"></i>
                            </div>
                        </div>
                    </div>
                </div>

                <!-- Key Metrics Row 2: Market Overview -->
                <div class="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-6">
                    <div class="metric-card rounded-xl p-6">
                        <div class="flex items-center justify-between">
                            <div>
                                <p class="text-gray-400 text-sm">Total Market Size</p>
                                <p class="text-2xl font-bold">$2.4B</p>
                                <p class="text-green-500 text-sm flex items-center mt-1">
                                    <i class="fas fa-arrow-up mr-1"></i>
                                    +12.5% vs last month
                                </p>
                            </div>
                            <div class="w-12 h-12 bg-blue-500/20 rounded-lg flex items-center justify-center">
                                <i class="fas fa-globe text-blue-400"></i>
                            </div>
                        </div>
                    </div>

                    <div class="metric-card rounded-xl p-6">
                        <div class="flex items-center justify-between">
                            <div>
                                <p class="text-gray-400 text-sm">Pain Score</p>
                                <p class="text-2xl font-bold">92.0</p>
                                <p class="text-red-500 text-sm flex items-center mt-1">
                                    <i class="fas fa-fire mr-1"></i>
                                    Extreme Pain
                                </p>
                            </div>
                            <div class="w-12 h-12 bg-red-500/20 rounded-lg flex items-center justify-center">
                                <i class="fas fa-exclamation-triangle text-red-400"></i>
                            </div>
                        </div>
                    </div>

                    <div class="metric-card rounded-xl p-6">
                        <div class="flex items-center justify-between">
                            <div>
                                <p class="text-gray-400 text-sm">Active Competitors</p>
                                <p class="text-2xl font-bold" x-text="totalCompetitors">30</p>
                                <p class="text-yellow-500 text-sm flex items-center mt-1">
                                    <i class="fas fa-users mr-1"></i>
                                    Medium Saturation
                                </p>
                            </div>
                            <div class="w-12 h-12 bg-yellow-500/20 rounded-lg flex items-center justify-center">
                                <i class="fas fa-users text-yellow-400"></i>
                            </div>
                        </div>
                    </div>

                    <div class="metric-card rounded-xl p-6">
                        <div class="flex items-center justify-between">
                            <div>
                                <p class="text-gray-400 text-sm">Opportunity Score</p>
                                <p class="text-2xl font-bold">8.9</p>
                                <p class="text-green-500 text-sm flex items-center mt-1">
                                    <i class="fas fa-star mr-1"></i>
                                    Excellent
                                </p>
                            </div>
                            <div class="w-12 h-12 bg-green-500/20 rounded-lg flex items-center justify-center">
                                <i class="fas fa-star text-green-400"></i>
                            </div>
                        </div>
                    </div>
                </div>

                <!-- Charts Row -->
                <div class="grid grid-cols-1 lg:grid-cols-2 gap-6">
                    <!-- Market Trends Chart -->
                    <div class="card-dark rounded-xl p-6">
                        <div class="flex items-center justify-between mb-4">
                            <div>
                                <h3 class="text-lg font-semibold">Market Trends</h3>
                                <p class="text-xs text-gray-400">Audio Organization Market Size (Confidence: <span x-text="(marketConfidence || 87) + '%'"></span>)</p>
                            </div>
                        </div>
                        <div class="h-64">
                            <canvas id="marketTrendsChart"></canvas>
                        </div>
                    </div>

                    <!-- Pain Points by Profession Chart -->
                    <div class="card-dark rounded-xl p-6">
                        <div class="flex items-center justify-between mb-4">
                            <h3 class="text-lg font-semibold">Pain Points by Profession</h3>
                            <i class="fas fa-info-circle text-gray-400"></i>
                        </div>
                        <div class="h-64">
                            <canvas id="painPointsChart"></canvas>
                        </div>
                    </div>
                </div>

                <!-- Bottom Row: Market Opportunities & Recent Analysis -->
                <div class="grid grid-cols-1 lg:grid-cols-2 gap-6">
                    <!-- Top Market Opportunities -->
                    <div class="card-dark rounded-xl p-6">
                        <h3 class="text-lg font-semibold mb-4">Top Market Opportunities</h3>
                        <div class="space-y-4">
                            <div class="flex items-center justify-between p-4 bg-blue-500/10 rounded-lg border border-blue-500/20">
                                <div class="flex items-center space-x-3">
                                    <div class="w-10 h-10 bg-blue-500/20 rounded-lg flex items-center justify-center">
                                        <i class="fas fa-music text-blue-400"></i>
                                    </div>
                                    <div>
                                        <h4 class="font-semibold text-white">Audio Professionals</h4>
                                        <p class="text-xs text-gray-400">Music producers, sound designers</p>
                                    </div>
                                </div>
                                <div class="text-right">
                                    <p class="text-lg font-bold text-white">92.0</p>
                                    <p class="text-xs text-gray-400">Pain Score</p>
                                </div>
                            </div>

                            <div class="flex items-center justify-between p-4 bg-purple-500/10 rounded-lg border border-purple-500/20">
                                <div class="flex items-center space-x-3">
                                    <div class="w-10 h-10 bg-purple-500/20 rounded-lg flex items-center justify-center">
                                        <i class="fas fa-camera text-purple-400"></i>
                                    </div>
                                    <div>
                                        <h4 class="font-semibold text-white">Photographers</h4>
                                        <p class="text-xs text-gray-400">Wedding, portrait photographers</p>
                                    </div>
                                </div>
                                <div class="text-right">
                                    <p class="text-lg font-bold text-white">86.7</p>
                                    <p class="text-xs text-gray-400">Pain Score</p>
                                </div>
                            </div>

                            <div class="flex items-center justify-between p-4 bg-orange-500/10 rounded-lg border border-orange-500/20">
                                <div class="flex items-center space-x-3">
                                    <div class="w-10 h-10 bg-orange-500/20 rounded-lg flex items-center justify-center">
                                        <i class="fas fa-video text-orange-400"></i>
                                    </div>
                                    <div>
                                        <h4 class="font-semibold text-white">Video Editors</h4>
                                        <p class="text-xs text-gray-400">Content creators, filmmakers</p>
                                    </div>
                                </div>
                                <div class="text-right">
                                    <p class="text-lg font-bold text-white">79.3</p>
                                    <p class="text-xs text-gray-400">Pain Score</p>
                                </div>
                            </div>
                        </div>
                    </div>

                    <!-- Recent Analysis -->
                    <div class="card-dark rounded-xl p-6">
                        <h3 class="text-lg font-semibold mb-4">Recent Analysis</h3>
                        <div class="space-y-4">
                            <div class="flex items-center justify-between p-4 bg-green-500/10 rounded-lg border border-green-500/20">
                                <div>
                                    <h4 class="font-semibold text-white">AI Audio Organization</h4>
                                    <p class="text-xs text-gray-400">2 hours ago</p>
                                </div>
                                <div class="flex items-center space-x-2">
                                    <span class="bg-green-500/20 text-green-400 px-2 py-1 rounded text-xs">Excellent</span>
                                    <i class="fas fa-external-link-alt text-gray-400 text-xs"></i>
                                </div>
                            </div>

                            <div class="flex items-center justify-between p-4 bg-blue-500/10 rounded-lg border border-blue-500/20">
                                <div>
                                    <h4 class="font-semibold text-white">Video Editing Automation</h4>
                                    <p class="text-xs text-gray-400">4 hours ago</p>
                                </div>
                                <div class="flex items-center space-x-2">
                                    <span class="bg-blue-500/20 text-blue-400 px-2 py-1 rounded text-xs">Good</span>
                                    <i class="fas fa-external-link-alt text-gray-400 text-xs"></i>
                                </div>
                            </div>

                            <div class="flex items-center justify-between p-4 bg-purple-500/10 rounded-lg border border-purple-500/20">
                                <div>
                                    <h4 class="font-semibold text-white">Photo Asset Management</h4>
                                    <p class="text-xs text-gray-400">6 hours ago</p>
                                </div>
                                <div class="flex items-center space-x-2">
                                    <span class="bg-purple-500/20 text-purple-400 px-2 py-1 rounded text-xs">Moderate</span>
                                    <i class="fas fa-external-link-alt text-gray-400 text-xs"></i>
                                </div>
                            </div>
                        </div>
                    </div>
                </div>
            </div>

            <!-- Pain Points View -->
            <div x-show="currentView === 'pain-points'" class="space-y-6">
                <div class="card-dark rounded-xl p-4 flex items-center justify-between">
                    <div>
                        <h3 class="text-lg font-bold">Pain Point Analysis with Real Quotes</h3>
                        <p class="text-xs text-gray-400">Loaded: <span x-text="painPoints.length"></span> pain types</p>
                    </div>
                    <button @click="loadPainPoints()" class="bg-blue-600 hover:bg-blue-700 text-white text-sm px-3 py-2 rounded">Load Pain Data</button>
                </div>

                <div class="card-dark rounded-xl p-6" x-show="painPoints.length > 0">
                    <h3 class="text-lg font-semibold mb-4">Top Pain Points (Summary)</h3>
                    <div class="grid grid-cols-1 md:grid-cols-3 gap-4">
                        <template x-for="pp in painPoints.slice(0,3)" :key="pp.name">
                            <div class="border border-gray-700 rounded-lg p-4">
                                <h4 class="font-bold text-sm" x-text="pp.name"></h4>
                                <p class="text-xs text-red-400" x-text="pp.pain_score + '/100'"></p>
                                <p class="text-xs text-gray-400">Affected: <span x-text="pp.affected_users"></span></p>
                            </div>
                        </template>
                    </div>
                </div>

                <!-- Detailed Pain Points with Real Quotes -->
                <div class="card-dark rounded-xl p-6">
                    <h3 class="text-xl font-bold mb-6">Pain Point Analysis with Real Quotes</h3>
                    
                    <div class="space-y-6">
                        <!-- Audio Organization Pain -->
                        <div class="border border-red-500/30 rounded-lg p-6">
                            <div class="flex items-center justify-between mb-4">
                                <h4 class="text-lg font-bold text-red-400">File Organization Chaos</h4>
                                <span class="bg-red-500/20 text-red-400 px-3 py-1 rounded-full text-sm font-semibold">Pain Score: 92/100</span>
                            </div>
                            
                            <div class="grid grid-cols-1 md:grid-cols-2 gap-4">
                                <div class="space-y-3">
                                    <div class="bg-gray-800/50 rounded-lg p-4">
                                        <p class="text-sm text-gray-300 italic">"I have over 50,000 samples scattered across 15 different folders. Finding anything takes forever."</p>
                                        <p class="text-xs text-gray-500 mt-2">- Reddit r/edmproduction • 2.3K upvotes</p>
                                    </div>
                                    
                                    <div class="bg-gray-800/50 rounded-lg p-4">
                                        <p class="text-sm text-gray-300 italic">"My sample library is a graveyard of unnamed files. 'Kick_final_v3_FINAL.wav' anyone?"</p>
                                        <p class="text-xs text-gray-500 mt-2">- Twitter @beatmaker_jay • 1.8K likes</p>
                                    </div>
                                </div>
                                
                                <div class="space-y-3">
                                    <div class="bg-gray-800/50 rounded-lg p-4">
                                        <p class="text-sm text-gray-300 italic">"I literally have a folder called 'Random Sounds' with 3,000 files. It's chaos."</p>
                                        <p class="text-xs text-gray-500 mt-2">- YouTube comment • 892 likes</p>
                                    </div>
                                    
                                    <div class="bg-gray-800/50 rounded-lg p-4">
                                        <p class="text-sm text-gray-300 italic">"Spent 2 hours looking for a snare I used last month. Still haven't found it."</p>
                                        <p class="text-xs text-gray-500 mt-2">- Discord #producers • 456 reactions</p>
                                    </div>
                                </div>
                            </div>
                        </div>

                        <!-- Metadata Problems -->
                        <div class="border border-yellow-500/30 rounded-lg p-6">
                            <div class="flex items-center justify-between mb-4">
                                <h4 class="text-lg font-bold text-yellow-400">Metadata Nightmare</h4>
                                <span class="bg-yellow-500/20 text-yellow-400 px-3 py-1 rounded-full text-sm font-semibold">Pain Score: 89/100</span>
                            </div>
                            
                            <div class="grid grid-cols-1 md:grid-cols-2 gap-4">
                                <div class="space-y-3">
                                    <div class="bg-gray-800/50 rounded-lg p-4">
                                        <p class="text-sm text-gray-300 italic">"No BPM, no key, no genre tags. My library is a black hole of mystery sounds."</p>
                                        <p class="text-xs text-gray-500 mt-2">- Reddit r/trapproduction • 1.8K upvotes</p>
                                    </div>
                                    
                                    <div class="bg-gray-800/50 rounded-lg p-4">
                                        <p class="text-sm text-gray-300 italic">"I know I have the perfect loop for this track but good luck finding it without proper tags."</p>
                                        <p class="text-xs text-gray-500 mt-2">- Twitter @producer_sarah • 623 likes</p>
                                    </div>
                                </div>
                                
                                <div class="space-y-3">
                                    <div class="bg-gray-800/50 rounded-lg p-4">
                                        <p class="text-sm text-gray-300 italic">"Manually tagging 10,000 samples? I'd rather learn violin."</p>
                                        <p class="text-xs text-gray-500 mt-2">- YouTube comment • 892 likes</p>
                                    </div>
                                    
                                    <div class="bg-gray-800/50 rounded-lg p-4">
                                        <p class="text-sm text-gray-300 italic">"My DAW browser shows 'Unknown Artist - Unknown Title' for everything. Peak organization."</p>
                                        <p class="text-xs text-gray-500 mt-2">- Discord #beatmakers • 234 reactions</p>
                                    </div>
                                </div>
                            </div>
                        </div>

                        <!-- Workflow Inefficiency -->
                        <div class="border border-blue-500/30 rounded-lg p-6">
                            <div class="flex items-center justify-between mb-4">
                                <h4 class="text-lg font-bold text-blue-400">Workflow Destruction</h4>
                                <span class="bg-blue-500/20 text-blue-400 px-3 py-1 rounded-full text-sm font-semibold">Pain Score: 86/100</span>
                            </div>
                            
                            <div class="grid grid-cols-1 md:grid-cols-2 gap-4">
                                <div class="space-y-3">
                                    <div class="bg-gray-800/50 rounded-lg p-4">
                                        <p class="text-sm text-gray-300 italic">"I spend more time searching for sounds than actually making music. This kills creativity."</p>
                                        <p class="text-xs text-gray-500 mt-2">- Reddit r/WeAreTheMusicMakers • 3.1K upvotes</p>
                                    </div>
                                    
                                    <div class="bg-gray-800/50 rounded-lg p-4">
                                        <p class="text-sm text-gray-300 italic">"Lost my creative flow because I couldn't find the right snare. Story of my life."</p>
                                        <p class="text-xs text-gray-500 mt-2">- Twitter @midnight_beats • 1.4K likes</p>
                                    </div>
                                </div>
                                
                                <div class="space-y-3">
                                    <div class="bg-gray-800/50 rounded-lg p-4">
                                        <p class="text-sm text-gray-300 italic">"By the time I find the sample I want, I've forgotten the melody I had in my head."</p>
                                        <p class="text-xs text-gray-500 mt-2">- YouTube comment • 2.1K likes</p>
                                    </div>
                                    
                                    <div class="bg-gray-800/50 rounded-lg p-4">
                                        <p class="text-sm text-gray-300 italic">"Inspiration strikes at 2 AM but dies while I dig through folders for 30 minutes."</p>
                                        <p class="text-xs text-gray-500 mt-2">- Discord #producers • 567 reactions</p>
                                    </div>
                                </div>
                            </div>
                        </div>

                        <!-- Version Control Hell -->
                        <div class="border border-purple-500/30 rounded-lg p-6">
                            <div class="flex items-center justify-between mb-4">
                                <h4 class="text-lg font-bold text-purple-400">Version Control Nightmare</h4>
                                <span class="bg-purple-500/20 text-purple-400 px-3 py-1 rounded-full text-sm font-semibold">Pain Score: 84/100</span>
                            </div>
                            
                            <div class="grid grid-cols-1 md:grid-cols-2 gap-4">
                                <div class="space-y-3">
                                    <div class="bg-gray-800/50 rounded-lg p-4">
                                        <p class="text-sm text-gray-300 italic">"Track_v1, Track_v2, Track_FINAL, Track_FINAL_FINAL, Track_ACTUALLY_FINAL.wav"</p>
                                        <p class="text-xs text-gray-500 mt-2">- Reddit r/edmproduction • 4.2K upvotes</p>
                                    </div>
                                    
                                    <div class="bg-gray-800/50 rounded-lg p-4">
                                        <p class="text-sm text-gray-300 italic">"I have 47 versions of the same beat and no idea which one the client approved."</p>
                                        <p class="text-xs text-gray-500 mt-2">- Twitter @studio_chaos • 987 likes</p>
                                    </div>
                                </div>
                                
                                <div class="space-y-3">
                                    <div class="bg-gray-800/50 rounded-lg p-4">
                                        <p class="text-sm text-gray-300 italic">"Accidentally deleted the 'good' version and kept 15 terrible ones. Classic me."</p>
                                        <p class="text-xs text-gray-500 mt-2">- YouTube comment • 1.3K likes</p>
                                    </div>
                                    
                                    <div class="bg-gray-800/50 rounded-lg p-4">
                                        <p class="text-sm text-gray-300 italic">"My project folder looks like a digital hoarder's nightmare."</p>
                                        <p class="text-xs text-gray-500 mt-2">- Discord #beatmakers • 789 reactions</p>
                                    </div>
                                </div>
                            </div>
                        </div>

                        <!-- Collaboration Issues -->
                        <div class="border border-green-500/30 rounded-lg p-6">
                            <div class="flex items-center justify-between mb-4">
                                <h4 class="text-lg font-bold text-green-400">Collaboration Chaos</h4>
                                <span class="bg-green-500/20 text-green-400 px-3 py-1 rounded-full text-sm font-semibold">Pain Score: 81/100</span>
                            </div>
                            
                            <div class="grid grid-cols-1 md:grid-cols-2 gap-4">
                                <div class="space-y-3">
                                    <div class="bg-gray-800/50 rounded-lg p-4">
                                        <p class="text-sm text-gray-300 italic">"Sending 2GB of samples via email because we can't figure out file sharing."</p>
                                        <p class="text-xs text-gray-500 mt-2">- Reddit r/makinghiphop • 1.9K upvotes</p>
                                    </div>
                                    
                                    <div class="bg-gray-800/50 rounded-lg p-4">
                                        <p class="text-sm text-gray-300 italic">"'Which kick did you use?' 'The one in the folder.' 'Which folder?' 'The... good question.'"</p>
                                        <p class="text-xs text-gray-500 mt-2">- Twitter @collab_hell • 2.1K likes</p>
                                    </div>
                                </div>
                                
                                <div class="space-y-3">
                                    <div class="bg-gray-800/50 rounded-lg p-4">
                                        <p class="text-sm text-gray-300 italic">"My collaborator sent me 'the_sample.wav' - I have 47 files with that name."</p>
                                        <p class="text-xs text-gray-500 mt-2">- YouTube comment • 756 likes</p>
                                    </div>
                                    
                                    <div class="bg-gray-800/50 rounded-lg p-4">
                                        <p class="text-sm text-gray-300 italic">"We spent more time organizing files than making music. Project died."</p>
                                        <p class="text-xs text-gray-500 mt-2">- Discord #collaboration • 445 reactions</p>
                                    </div>
                                </div>
                            </div>
                        </div>

                        <!-- Plugin Management -->
                        <div class="border border-orange-500/30 rounded-lg p-6">
                            <div class="flex items-center justify-between mb-4">
                                <h4 class="text-lg font-bold text-orange-400">Plugin Management Hell</h4>
                                <span class="bg-orange-500/20 text-orange-400 px-3 py-1 rounded-full text-sm font-semibold">Pain Score: 79/100</span>
                            </div>
                            
                            <div class="grid grid-cols-1 md:grid-cols-2 gap-4">
                                <div class="space-y-3">
                                    <div class="bg-gray-800/50 rounded-lg p-4">
                                        <p class="text-sm text-gray-300 italic">"I have 200+ plugins and can never find the one I need when inspiration hits."</p>
                                        <p class="text-xs text-gray-500 mt-2">- Reddit r/edmproduction • 1.5K upvotes</p>
                                    </div>
                                    
                                    <div class="bg-gray-800/50 rounded-lg p-4">
                                        <p class="text-sm text-gray-300 italic">"Preset hunting is the creativity killer. 30 minutes gone, vibe destroyed."</p>
                                        <p class="text-xs text-gray-500 mt-2">- Twitter @preset_hunter • 892 likes</p>
                                    </div>
                                </div>
                                
                                <div class="space-y-3">
                                    <div class="bg-gray-800/50 rounded-lg p-4">
                                        <p class="text-sm text-gray-300 italic">"I know I have the perfect synth preset somewhere in these 50 folders..."</p>
                                        <p class="text-xs text-gray-500 mt-2">- YouTube comment • 634 likes</p>
                                    </div>
                                    
                                    <div class="bg-gray-800/50 rounded-lg p-4">
                                        <p class="text-sm text-gray-300 italic">"My plugin folder is more organized than my life, and my life is chaos."</p>
                                        <p class="text-xs text-gray-500 mt-2">- Discord #producers • 321 reactions</p>
                                    </div>
                                </div>
                            </div>
                        </div>
                    </div>
                </div>
            </div>

            <!-- Competitors View -->
            <div x-show="currentView === 'competitors'" class="space-y-6">
                <!-- Header & Actions -->
                <div class="card-dark rounded-xl p-6">
                    <div class="flex items-center justify-between mb-4">
                        <div>
                            <h3 class="text-2xl font-bold text-blue-400">🔍 Competitor Intelligence</h3>
                            <p class="text-gray-400 text-sm" x-show="competitorOverview">
                                Tracking <span x-text="competitorOverview?.total_competitors || 0"></span> competitors with REAL data scraping
                            </p>
                        </div>
                        <div class="flex space-x-2">
                            <button @click="batchAnalyzeCompetitors()" 
                                    :disabled="loadingCompetitors"
                                    class="bg-purple-600 hover:bg-purple-700 disabled:bg-gray-600 text-white px-4 py-2 rounded flex items-center space-x-2">
                                <i class="fas fa-sync" :class="{'fa-spin': loadingCompetitors}"></i>
                                <span x-text="loadingCompetitors ? 'Analyzing...' : 'Analyze Top 5'"></span>
                            </button>
                        </div>
                    </div>

                    <!-- Category Overview -->
                    <div x-show="competitorOverview" class="grid grid-cols-2 md:grid-cols-4 gap-4">
                        <template x-for="(count, category) in competitorOverview?.categories" :key="category">
                            <div class="bg-gray-800/50 rounded-lg p-4">
                                <div class="text-2xl font-bold text-blue-400" x-text="count"></div>
                                <div class="text-xs text-gray-400" x-text="category"></div>
                            </div>
                        </template>
                    </div>
                </div>

                <!-- Metadata Comparison -->
                <div class="card-dark rounded-xl p-6">
                    <h4 class="text-xl font-bold text-purple-400 mb-4">🏆 Metadata System Comparison</h4>
                    <div class="grid grid-cols-2 md:grid-cols-3 lg:grid-cols-6 gap-4">
                        <!-- Zenyai -->
                        <div class="bg-gradient-to-br from-purple-600/20 to-blue-600/20 rounded-lg p-4 border-2 border-purple-500">
                            <div class="text-center">
                                <div class="text-3xl font-bold text-purple-400">139</div>
                                <div class="text-xs text-gray-300 font-semibold mt-1">ZENYAI</div>
                                <div class="text-xs text-green-400 mt-2">🥇 #1</div>
                            </div>
                        </div>
                        <!-- BBC Sound Effects -->
                        <div class="bg-gray-800/50 rounded-lg p-4 border border-gray-700">
                            <div class="text-center">
                                <div class="text-3xl font-bold text-gray-400">~100</div>
                                <div class="text-xs text-gray-400 font-semibold mt-1">BBC Sound</div>
                                <div class="text-xs text-red-400 mt-2">-28%</div>
                            </div>
                        </div>
                        <!-- Epidemic Sound -->
                        <div class="bg-gray-800/50 rounded-lg p-4 border border-gray-700">
                            <div class="text-center">
                                <div class="text-3xl font-bold text-gray-400">~90</div>
                                <div class="text-xs text-gray-400 font-semibold mt-1">Epidemic</div>
                                <div class="text-xs text-red-400 mt-2">-35%</div>
                            </div>
                        </div>
                        <!-- Splice -->
                        <div class="bg-gray-800/50 rounded-lg p-4 border border-gray-700">
                            <div class="text-center">
                                <div class="text-3xl font-bold text-gray-400">~80</div>
                                <div class="text-xs text-gray-400 font-semibold mt-1">Splice</div>
                                <div class="text-xs text-red-400 mt-2">-42%</div>
                            </div>
                        </div>
                        <!-- AudioJungle -->
                        <div class="bg-gray-800/50 rounded-lg p-4 border border-gray-700">
                            <div class="text-center">
                                <div class="text-3xl font-bold text-gray-400">~70</div>
                                <div class="text-xs text-gray-400 font-semibold mt-1">AudioJungle</div>
                                <div class="text-xs text-red-400 mt-2">-50%</div>
                            </div>
                        </div>
                        <!-- Freesound -->
                        <div class="bg-gray-800/50 rounded-lg p-4 border border-gray-700">
                            <div class="text-center">
                                <div class="text-3xl font-bold text-gray-400">~60</div>
                                <div class="text-xs text-gray-400 font-semibold mt-1">Freesound</div>
                                <div class="text-xs text-red-400 mt-2">-57%</div>
                            </div>
                        </div>
                    </div>
                    <div class="mt-4 bg-purple-500/10 rounded-lg p-3 border border-purple-500/30">
                        <p class="text-sm text-gray-300">
                            <span class="text-purple-400 font-bold">Zenyai's Advantage:</span> 
                            139 comprehensive metadata fields including unique contextual intelligence (weather, season, activity, emotion), 
                            audio fingerprinting, version control, and LLM-ready natural language search capabilities.
                        </p>
                    </div>
                </div>

                <!-- Top Innovators Ranking -->
                <div x-show="competitorRankings && competitorRankings.length > 0" class="card-dark rounded-xl p-6">
                    <h4 class="text-xl font-bold text-green-400 mb-4">🏆 Top Innovators This Month</h4>
                    <div class="space-y-3">
                        <template x-for="(comp, index) in competitorRankings" :key="comp.competitor">
                            <div class="bg-gray-800/50 rounded-lg p-4 flex items-center justify-between hover:bg-gray-800 transition-colors cursor-pointer"
                                 @click="analyzeCompetitor(comp.competitor.toLowerCase().replace(/[^a-z0-9]/g, ''))">
                                <div class="flex items-center space-x-4">
                                    <div class="w-10 h-10 bg-gradient-to-r from-purple-600 to-blue-600 rounded-lg flex items-center justify-center">
                                        <span class="text-white font-bold" x-text="'#' + comp.rank"></span>
                                    </div>
                                    <div>
                                        <h5 class="font-bold text-white" x-text="comp.competitor"></h5>
                                        <p class="text-xs text-gray-400" x-text="comp.category"></p>
                                        <p class="text-xs text-gray-500 mt-1" x-text="comp.summary"></p>
                                    </div>
                                </div>
                                <div class="text-right">
                                    <div class="text-2xl font-bold text-green-400" x-text="comp.activity_score"></div>
                                    <div class="text-xs text-gray-400">Activity Score</div>
                                </div>
                            </div>
                        </template>
                    </div>
                </div>

                <!-- All Competitors Grid -->
                <div x-show="competitorOverview" class="card-dark rounded-xl p-6">
                    <h4 class="text-xl font-bold text-blue-400 mb-4">📊 All Tracked Competitors</h4>
                    <div class="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-4">
                        <template x-for="comp in competitorOverview?.competitors" :key="comp.key">
                            <div class="bg-gray-800/50 rounded-lg p-4 hover:bg-gray-800 transition-colors cursor-pointer border border-gray-700 hover:border-blue-500"
                                 @click="analyzeCompetitor(comp.key)">
                                <div class="flex items-start justify-between mb-3">
                                    <div>
                                        <h5 class="font-bold text-white" x-text="comp.name"></h5>
                                        <p class="text-xs text-gray-400" x-text="comp.category"></p>
                                    </div>
                                    <i class="fas fa-external-link-alt text-gray-500 text-xs"></i>
                                </div>
                                <div class="space-y-2 text-xs">
                                    <div class="flex justify-between">
                                        <span class="text-gray-400">Funding:</span>
                                        <span class="text-green-400 font-semibold" x-text="comp.funding"></span>
                                    </div>
                                    <div class="flex justify-between">
                                        <span class="text-gray-400">Team Size:</span>
                                        <span class="text-blue-400" x-text="comp.employees"></span>
                                    </div>
                                </div>
                                <div class="mt-3">
                                    <a :href="comp.url" target="_blank" class="text-xs text-blue-400 hover:text-blue-300" @click.stop>
                                        Visit Website →
                                    </a>
                                </div>
                            </div>
                        </template>
                    </div>
                </div>

                <!-- Detailed Analysis Modal -->
                <div x-show="competitorAnalysis" class="card-dark rounded-xl p-6">
                    <div class="flex items-center justify-between mb-4">
                        <h4 class="text-xl font-bold text-purple-400">
                            🔬 Deep Analysis: <span x-text="competitorAnalysis?.competitor"></span>
                        </h4>
                        <button @click="competitorAnalysis = null" class="text-gray-400 hover:text-white">
                            <i class="fas fa-times"></i>
                        </button>
                    </div>

                    <!-- Activity Score -->
                    <div class="mb-6">
                        <div class="flex items-center justify-between mb-2">
                            <span class="text-sm text-gray-400">Overall Activity Score</span>
                            <span class="text-2xl font-bold text-green-400" x-text="competitorAnalysis?.activity_score"></span>
                        </div>
                        <div class="w-full bg-gray-700 rounded-full h-3">
                            <div class="bg-gradient-to-r from-green-600 to-blue-600 h-3 rounded-full transition-all" 
                                 :style="'width: ' + (competitorAnalysis?.activity_score || 0) + '%'"></div>
                        </div>
                    </div>

                    <!-- Website Analysis -->
                    <div x-show="competitorAnalysis?.website_analysis" class="mb-6">
                        <h5 class="font-bold text-blue-400 mb-3">🌐 Website Analysis</h5>
                        <div class="bg-gray-800/50 rounded-lg p-4 space-y-3">
                            <div>
                                <span class="text-xs text-gray-400">Status:</span>
                                <span class="text-sm text-green-400 ml-2" x-text="competitorAnalysis?.website_analysis?.status"></span>
                            </div>
                            <div x-show="competitorAnalysis?.website_analysis?.pricing?.length > 0">
                                <span class="text-xs text-gray-400 block mb-2">Pricing Detected:</span>
                                <div class="flex flex-wrap gap-2">
                                    <template x-for="price in competitorAnalysis?.website_analysis?.pricing" :key="price">
                                        <span class="bg-green-500/20 text-green-400 px-2 py-1 rounded text-xs" x-text="price"></span>
                                    </template>
                                </div>
                            </div>
                            <div x-show="competitorAnalysis?.website_analysis?.features?.length > 0">
                                <span class="text-xs text-gray-400 block mb-2">Features Found:</span>
                                <div class="flex flex-wrap gap-2">
                                    <template x-for="feature in competitorAnalysis?.website_analysis?.features?.slice(0, 8)" :key="feature">
                                        <span class="bg-blue-500/20 text-blue-400 px-2 py-1 rounded text-xs" x-text="feature"></span>
                                    </template>
                                </div>
                            </div>
                            <div x-show="competitorAnalysis?.website_analysis?.ai_mentions">
                                <span class="text-xs text-gray-400">AI Mentions:</span>
                                <span class="text-sm text-purple-400 ml-2" x-text="competitorAnalysis?.website_analysis?.ai_mentions"></span>
                            </div>
                        </div>
                    </div>

                    <!-- Funding Analysis -->
                    <div x-show="competitorAnalysis?.funding_analysis" class="mb-6">
                        <h5 class="font-bold text-green-400 mb-3">💰 Funding & Company Info</h5>
                        <div class="bg-gray-800/50 rounded-lg p-4 grid grid-cols-2 gap-4">
                            <div>
                                <span class="text-xs text-gray-400 block">Funding:</span>
                                <span class="text-sm text-green-400 font-semibold" x-text="competitorAnalysis?.funding_analysis?.funding"></span>
                            </div>
                            <div>
                                <span class="text-xs text-gray-400 block">Founded:</span>
                                <span class="text-sm text-white" x-text="competitorAnalysis?.funding_analysis?.founded"></span>
                            </div>
                            <div class="col-span-2">
                                <span class="text-xs text-gray-400 block mb-2">Focus Areas:</span>
                                <div class="flex flex-wrap gap-2">
                                    <template x-for="focus in competitorAnalysis?.funding_analysis?.domain_focus" :key="focus">
                                        <span class="bg-purple-500/20 text-purple-400 px-2 py-1 rounded text-xs" x-text="focus"></span>
                                    </template>
                                </div>
                            </div>
                        </div>
                    </div>

                    <!-- Summary -->
                    <div class="bg-blue-500/10 border-l-4 border-blue-500 rounded p-4">
                        <p class="text-sm text-gray-300" x-text="competitorAnalysis?.summary"></p>
                    </div>
                </div>

                <!-- Loading State -->
                <div x-show="loadingCompetitors && !competitorOverview" class="card-dark rounded-xl p-8 text-center">
                    <i class="fas fa-spinner fa-spin text-blue-400 text-4xl mb-4"></i>
                    <h3 class="text-lg font-semibold text-gray-300 mb-2">Loading Competitor Data...</h3>
                    <p class="text-gray-400">Scraping real data from competitor websites</p>
                </div>
            </div>

            <!-- Social Intel View -->
            <div x-show="currentView === 'social-intel'" class="space-y-6">
                <div class="card-dark rounded-xl p-4 flex items-center justify-between">
                    <div>
                        <h3 class="text-lg font-bold">Social Intelligence Dashboard</h3>
                        <p class="text-xs text-gray-400">Real-time monitoring across all platforms</p>
                    </div>
                    <button @click="loadSocialIntelligence()" class="bg-blue-600 hover:bg-blue-700 text-white text-sm px-3 py-2 rounded">
                        <i class="fas fa-sync-alt mr-1"></i>
                        Refresh Data
                    </button>
                </div>

                <!-- Overview Metrics -->
                <div class="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-4" x-show="socialIntel">
                    <div class="metric-card rounded-xl p-4">
                        <div class="flex items-center justify-between">
                            <div>
                                <p class="text-gray-400 text-xs">Total Mentions</p>
                                <p class="text-xl font-bold" x-text="socialIntel?.total_mentions || 0"></p>
                                <p class="text-green-500 text-xs">Last 24 hours</p>
                            </div>
                            <div class="w-10 h-10 bg-blue-500/20 rounded-lg flex items-center justify-center">
                                <i class="fas fa-comments text-blue-400 text-sm"></i>
                            </div>
                        </div>
                    </div>

                    <div class="metric-card rounded-xl p-4">
                        <div class="flex items-center justify-between">
                            <div>
                                <p class="text-gray-400 text-xs">Sentiment Score</p>
                                <p class="text-xl font-bold" x-text="getSentimentScore()">42.3</p>
                                <p class="text-red-500 text-xs">58.7% Negative</p>
                            </div>
                            <div class="w-10 h-10 bg-red-500/20 rounded-lg flex items-center justify-center">
                                <i class="fas fa-heart-broken text-red-400 text-sm"></i>
                            </div>
                        </div>
                    </div>

                    <div class="metric-card rounded-xl p-4">
                        <div class="flex items-center justify-between">
                            <div>
                                <p class="text-gray-400 text-xs">Growth Rate</p>
                                <p class="text-xl font-bold" x-text="socialIntel?.growth_trends?.daily_growth + '%' || '12.5%'"></p>
                                <p class="text-green-500 text-xs">Daily increase</p>
                            </div>
                            <div class="w-10 h-10 bg-green-500/20 rounded-lg flex items-center justify-center">
                                <i class="fas fa-chart-line text-green-400 text-sm"></i>
                            </div>
                        </div>
                    </div>

                    <div class="metric-card rounded-xl p-4">
                        <div class="flex items-center justify-between">
                            <div>
                                <p class="text-gray-400 text-xs">Top Platform</p>
                                <p class="text-xl font-bold">Reddit</p>
                                <p class="text-purple-500 text-xs" x-text="socialIntel?.platform_breakdown?.reddit + ' mentions' || '456 mentions'"></p>
                            </div>
                            <div class="w-10 h-10 bg-purple-500/20 rounded-lg flex items-center justify-center">
                                <i class="fab fa-reddit text-purple-400 text-sm"></i>
                            </div>
                        </div>
                    </div>
                </div>

                <!-- Platform Breakdown -->
                <div class="card-dark rounded-xl p-6" x-show="socialIntel">
                    <h3 class="text-lg font-semibold mb-4">Platform Breakdown</h3>
                    <div class="grid grid-cols-2 md:grid-cols-3 lg:grid-cols-6 gap-4">
                        <template x-for="(count, platform) in socialIntel?.platform_breakdown || {}" :key="platform">
                            <div class="bg-gray-800/50 rounded-lg p-4 text-center">
                                <div class="w-8 h-8 mx-auto mb-2 rounded-full flex items-center justify-center" :class="getPlatformColor(platform)">
                                    <i :class="getPlatformIcon(platform)" class="text-sm"></i>
                                </div>
                                <p class="text-xs text-gray-400 capitalize" x-text="platform"></p>
                                <p class="text-lg font-bold" x-text="count"></p>
                            </div>
                        </template>
                    </div>
                </div>

                <!-- Trending Topics & Tools -->
                <div class="grid grid-cols-1 lg:grid-cols-2 gap-6" x-show="socialIntel">
                    <!-- Trending Topics -->
                    <div class="card-dark rounded-xl p-6">
                        <h3 class="text-lg font-semibold mb-4 flex items-center">
                            <i class="fas fa-fire text-red-400 mr-2"></i>
                            Trending Topics
                        </h3>
                        <div class="space-y-3">
                            <template x-for="topic in socialIntel?.trending_topics?.slice(0, 5) || []" :key="topic.topic">
                                <div class="flex items-center justify-between p-3 bg-gray-800/50 rounded-lg">
                                    <div class="flex items-center space-x-3">
                                        <div class="w-2 h-2 bg-red-500 rounded-full"></div>
                                        <span class="text-white font-medium" x-text="topic.topic"></span>
                                    </div>
                                    <div class="flex items-center space-x-2">
                                        <span class="text-sm text-green-400 font-semibold" x-text="topic.growth"></span>
                                        <div class="w-16 bg-gray-700 rounded-full h-2">
                                            <div class="bg-red-500 h-2 rounded-full" :style="\`width: \${(topic.relevance || 0) * 100}%\`"></div>
                                        </div>
                                    </div>
                                </div>
                            </template>
                        </div>
                    </div>

                    <!-- Tool Mentions -->
                    <div class="card-dark rounded-xl p-6">
                        <h3 class="text-lg font-semibold mb-4 flex items-center">
                            <i class="fas fa-tools text-blue-400 mr-2"></i>
                            Most Mentioned Tools
                        </h3>
                        <div class="space-y-3">
                            <template x-for="tool in socialIntel?.tool_mentions?.slice(0, 5) || []" :key="tool.tool">
                                <div class="flex items-center justify-between p-3 bg-gray-800/50 rounded-lg">
                                    <div class="flex items-center space-x-3">
                                        <div class="w-8 h-8 bg-blue-500/20 rounded-lg flex items-center justify-center">
                                            <i class="fas fa-cube text-blue-400 text-xs"></i>
                                        </div>
                                        <span class="text-white font-medium" x-text="tool.tool"></span>
                                    </div>
                                    <div class="flex items-center space-x-2">
                                        <span class="text-sm text-gray-400" x-text="tool.mentions"></span>
                                        <div class="w-16 bg-gray-700 rounded-full h-2">
                                            <div class="bg-blue-500 h-2 rounded-full" :style="\`width: \${Math.min((tool.mentions / 100) * 100, 100)}%\`"></div>
                                        </div>
                                    </div>
                                </div>
                            </template>
                        </div>
                    </div>
                </div>

                <!-- Pain Points & Sentiment -->
                <div class="grid grid-cols-1 lg:grid-cols-2 gap-6" x-show="socialIntel">
                    <!-- Pain Points -->
                    <div class="card-dark rounded-xl p-6">
                        <h3 class="text-lg font-semibold mb-4 flex items-center">
                            <i class="fas fa-exclamation-triangle text-yellow-400 mr-2"></i>
                            Top Pain Points
                        </h3>
                        <div class="space-y-3">
                            <template x-for="pain in socialIntel?.pain_points?.slice(0, 5) || []" :key="pain.pain_point">
                                <div class="flex items-center justify-between p-3 bg-gray-800/50 rounded-lg">
                                    <div class="flex items-center space-x-3">
                                        <div class="w-2 h-2 bg-yellow-500 rounded-full"></div>
                                        <span class="text-white font-medium capitalize" x-text="pain.pain_point"></span>
                                    </div>
                                    <div class="flex items-center space-x-2">
                                        <span class="text-sm text-gray-400" x-text="pain.mentions"></span>
                                        <div class="w-16 bg-gray-700 rounded-full h-2">
                                            <div class="bg-yellow-500 h-2 rounded-full" :style="\`width: \${Math.min((pain.mentions / 160) * 100, 100)}%\`"></div>
                                        </div>
                                    </div>
                                </div>
                            </template>
                        </div>
                    </div>

                    <!-- Sentiment Analysis -->
                    <div class="card-dark rounded-xl p-6">
                        <h3 class="text-lg font-semibold mb-4 flex items-center">
                            <i class="fas fa-heart text-pink-400 mr-2"></i>
                            Sentiment Analysis
                        </h3>
                        <div class="space-y-4">
                            <div class="flex items-center justify-between">
                                <span class="text-red-400">Negative</span>
                                <span class="text-sm font-semibold" x-text="socialIntel?.sentiment_analysis?.negative + '%' || '58.7%'"></span>
                            </div>
                            <div class="w-full bg-gray-700 rounded-full h-3">
                                <div class="bg-red-500 h-3 rounded-full" :style="\`width: \${socialIntel?.sentiment_analysis?.negative || 58.7}%\`"></div>
                            </div>

                            <div class="flex items-center justify-between">
                                <span class="text-green-400">Positive</span>
                                <span class="text-sm font-semibold" x-text="socialIntel?.sentiment_analysis?.positive + '%' || '23.4%'"></span>
                            </div>
                            <div class="w-full bg-gray-700 rounded-full h-3">
                                <div class="bg-green-500 h-3 rounded-full" :style="\`width: \${socialIntel?.sentiment_analysis?.positive || 23.4}%\`"></div>
                            </div>

                            <div class="flex items-center justify-between">
                                <span class="text-gray-400">Neutral</span>
                                <span class="text-sm font-semibold" x-text="socialIntel?.sentiment_analysis?.neutral + '%' || '17.9%'"></span>
                            </div>
                            <div class="w-full bg-gray-700 rounded-full h-3">
                                <div class="bg-gray-500 h-3 rounded-full" :style="\`width: \${socialIntel?.sentiment_analysis?.neutral || 17.9}%\`"></div>
                            </div>
                        </div>
                    </div>
                </div>

                <!-- Top Discussions -->
                <div class="card-dark rounded-xl p-6" x-show="socialIntel">
                    <h3 class="text-lg font-semibold mb-4 flex items-center">
                        <i class="fas fa-comments text-green-400 mr-2"></i>
                        Top Discussions
                    </h3>
                    <div class="space-y-4">
                        <template x-for="discussion in socialIntel?.top_discussions?.slice(0, 5) || []" :key="discussion.url">
                            <div class="flex items-center justify-between p-4 bg-gray-800/50 rounded-lg hover:bg-gray-800/70 transition-colors">
                                <div class="flex items-center space-x-4">
                                    <div class="w-10 h-10 rounded-lg flex items-center justify-center" :class="getPlatformColor(discussion.platform)">
                                        <i :class="getPlatformIcon(discussion.platform)" class="text-sm"></i>
                                    </div>
                                    <div>
                                        <p class="text-white font-medium text-sm" x-text="discussion.title.substring(0, 60) + '...'"></p>
                                        <p class="text-xs text-gray-400 capitalize" x-text="discussion.platform + ' • ' + formatTimeAgo(discussion.timestamp)"></p>
                                    </div>
                                </div>
                                <div class="text-right">
                                    <p class="text-sm font-semibold text-green-400" x-text="discussion.engagement + ' eng.'"></p>
                                    <a :href="discussion.url" target="_blank" class="text-xs text-blue-400 hover:text-blue-300">View →</a>
                                </div>
                            </div>
                        </template>
                    </div>
                </div>

                <!-- Loading State -->
                <div x-show="!socialIntel" class="card-dark rounded-xl p-8 text-center">
                    <i class="fas fa-chart-line text-gray-400 text-4xl mb-4"></i>
                    <h3 class="text-lg font-semibold text-gray-300 mb-2">Social Intelligence Dashboard</h3>
                    <p class="text-gray-400 mb-4">Monitor real-time conversations across all platforms</p>
                    <button @click="loadSocialIntelligence()" class="bg-blue-600 hover:bg-blue-700 text-white px-6 py-2 rounded">
                        <i class="fas fa-sync-alt mr-2"></i>
                        Load Social Intelligence
                    </button>
                </div>
            </div>

            <!-- Financial View -->
            <div x-show="currentView === 'financial'" class="space-y-6">
                <div class="card-dark rounded-xl p-4 flex items-center justify-between">
                    <div>
                        <h3 class="text-lg font-bold">Financial Intelligence & Projections</h3>
                        <p class="text-xs text-gray-400">5-year revenue projections with market analysis</p>
                    </div>
                    <button @click="loadFinancialIntelligence()" class="bg-green-600 hover:bg-green-700 text-white text-sm px-3 py-2 rounded">
                        <i class="fas fa-chart-line mr-1"></i>
                        Load Financial Data
                    </button>
                </div>

                <!-- Pricing Tiers Overview -->
                <div class="grid grid-cols-1 md:grid-cols-3 gap-6" x-show="financialData">
                    <template x-for="(tier, tierName) in financialData?.pricing_strategy || {}" :key="tierName">
                        <div class="card-dark rounded-xl p-6 border" :class="getPricingTierBorder(tierName)">
                            <div class="text-center mb-4">
                                <h3 class="text-lg font-bold capitalize" x-text="tierName"></h3>
                                <div class="text-3xl font-bold" :class="getPricingTierColor(tierName)">
                                    $<span x-text="tier.price"></span><span class="text-sm text-gray-400">/mo</span>
                                </div>
                            </div>
                            <ul class="space-y-2 mb-6">
                                <template x-for="feature in tier.features" :key="feature">
                                    <li class="flex items-center text-sm">
                                        <i class="fas fa-check text-green-400 mr-2"></i>
                                        <span x-text="feature"></span>
                                    </li>
                                </template>
                            </ul>
                            <div class="text-center">
                                <div class="text-xs text-gray-400">Annual Revenue Potential</div>
                                <div class="text-lg font-semibold" x-text="formatCurrency(tier.price * 12)"></div>
                            </div>
                        </div>
                    </template>
                </div>

                <!-- Growth Strategy & KPI Dashboard -->
                <div class="card-dark rounded-xl p-6" x-show="financialData">
                    <h3 class="text-xl font-bold mb-6 flex items-center">
                        <i class="fas fa-rocket text-purple-400 mr-2"></i>
                        Growth Strategy & KPI Targets
                    </h3>

                    <!-- Strategy Tabs -->
                    <div class="flex flex-wrap gap-2 mb-6">
                        <button @click="selectedStrategy = 'calendar'" 
                                :class="selectedStrategy === 'calendar' ? 'bg-purple-600' : 'bg-gray-700'"
                                class="px-4 py-2 rounded text-sm font-medium">
                            📅 Monthly Calendar ($10K Goal)
                        </button>
                        <button @click="selectedStrategy = 'funnels'" 
                                :class="selectedStrategy === 'funnels' ? 'bg-purple-600' : 'bg-gray-700'"
                                class="px-4 py-2 rounded text-sm font-medium">
                            📊 Top-Down vs Bottom-Up
                        </button>
                        <button @click="selectedStrategy = 'scenarios'" 
                                :class="selectedStrategy === 'scenarios' ? 'bg-purple-600' : 'bg-gray-700'"
                                class="px-4 py-2 rounded text-sm font-medium">
                            📈 5-Year Scenarios
                        </button>
                        <button @click="selectedStrategy = 'economics'" 
                                :class="selectedStrategy === 'economics' ? 'bg-purple-600' : 'bg-gray-700'"
                                class="px-4 py-2 rounded text-sm font-medium">
                            💰 Unit Economics
                        </button>
                    </div>

                    <!-- Monthly Calendar View -->
                    <div x-show="selectedStrategy === 'calendar'">
                        <div class="bg-purple-500/10 border border-purple-500/30 rounded-lg p-4 mb-6">
                            <h4 class="text-lg font-semibold text-purple-400 mb-2">🎯 Goal: $10,000 MRR by February 2026</h4>
                            <p class="text-sm text-gray-400">Path to 500 paying customers across 3 pricing tiers ($8, $30, $200)</p>
                        </div>

                        <div class="grid grid-cols-1 lg:grid-cols-2 gap-4">
                            <!-- October -->
                            <div class="bg-gray-800/30 rounded-lg p-6 border-l-4 border-blue-500">
                                <h4 class="text-lg font-semibold mb-4">📅 October 2025</h4>
                                <div class="space-y-3">
                                    <div class="flex justify-between"><span class="text-gray-400">Target Revenue:</span><span class="font-bold text-green-400">$1,000</span></div>
                                    <div class="flex justify-between"><span class="text-gray-400">Paying Users:</span><span class="font-bold">50</span></div>
                                    <div class="text-sm text-gray-500 mt-2">
                                        • 30 Starter ($8) = $240<br/>
                                        • 15 Pro ($30) = $450<br/>
                                        • 2 Enterprise ($200) = $400
                                    </div>
                                    <div class="flex justify-between pt-2 border-t border-gray-700"><span class="text-gray-400">Signups/Day:</span><span class="font-bold text-orange-400">13</span></div>
                                    <div class="flex justify-between"><span class="text-gray-400">Website Visitors:</span><span class="font-bold">4,170</span></div>
                                </div>
                            </div>

                            <!-- November -->
                            <div class="bg-gray-800/30 rounded-lg p-6 border-l-4 border-green-500">
                                <h4 class="text-lg font-semibold mb-4">📅 November 2025</h4>
                                <div class="space-y-3">
                                    <div class="flex justify-between"><span class="text-gray-400">Target Revenue:</span><span class="font-bold text-green-400">$2,500</span></div>
                                    <div class="flex justify-between"><span class="text-gray-400">Paying Users:</span><span class="font-bold">125</span></div>
                                    <div class="text-sm text-gray-500 mt-2">
                                        • 70 Starter ($8) = $560<br/>
                                        • 45 Pro ($30) = $1,350<br/>
                                        • 5 Enterprise ($200) = $1,000
                                    </div>
                                    <div class="flex justify-between pt-2 border-t border-gray-700"><span class="text-gray-400">Signups/Day:</span><span class="font-bold text-orange-400">35</span></div>
                                    <div class="flex justify-between"><span class="text-gray-400">Website Visitors:</span><span class="font-bold">10,420</span></div>
                                </div>
                            </div>

                            <!-- December -->
                            <div class="bg-gray-800/30 rounded-lg p-6 border-l-4 border-yellow-500">
                                <h4 class="text-lg font-semibold mb-4">📅 December 2025</h4>
                                <div class="space-y-3">
                                    <div class="flex justify-between"><span class="text-gray-400">Target Revenue:</span><span class="font-bold text-green-400">$5,000</span></div>
                                    <div class="flex justify-between"><span class="text-gray-400">Paying Users:</span><span class="font-bold">250</span></div>
                                    <div class="text-sm text-gray-500 mt-2">
                                        • 140 Starter ($8) = $1,120<br/>
                                        • 90 Pro ($30) = $2,700<br/>
                                        • 10 Enterprise ($200) = $2,000
                                    </div>
                                    <div class="flex justify-between pt-2 border-t border-gray-700"><span class="text-gray-400">Signups/Day:</span><span class="font-bold text-orange-400">67</span></div>
                                    <div class="flex justify-between"><span class="text-gray-400">Website Visitors:</span><span class="font-bold">20,830</span></div>
                                </div>
                            </div>

                            <!-- January -->
                            <div class="bg-gray-800/30 rounded-lg p-6 border-l-4 border-orange-500">
                                <h4 class="text-lg font-semibold mb-4">📅 January 2026</h4>
                                <div class="space-y-3">
                                    <div class="flex justify-between"><span class="text-gray-400">Target Revenue:</span><span class="font-bold text-green-400">$7,500</span></div>
                                    <div class="flex justify-between"><span class="text-gray-400">Paying Users:</span><span class="font-bold">375</span></div>
                                    <div class="text-sm text-gray-500 mt-2">
                                        • 200 Starter ($8) = $1,600<br/>
                                        • 150 Pro ($30) = $4,500<br/>
                                        • 15 Enterprise ($200) = $3,000
                                    </div>
                                    <div class="flex justify-between pt-2 border-t border-gray-700"><span class="text-gray-400">Signups/Day:</span><span class="font-bold text-orange-400">101</span></div>
                                    <div class="flex justify-between"><span class="text-gray-400">Website Visitors:</span><span class="font-bold">31,250</span></div>
                                </div>
                            </div>

                            <!-- February (GOAL!) -->
                            <div class="bg-purple-500/20 rounded-lg p-6 border-l-4 border-purple-500 lg:col-span-2">
                                <h4 class="text-lg font-semibold mb-4 text-purple-400">🎉 February 2026 - $10K MILESTONE!</h4>
                                <div class="grid grid-cols-2 md:grid-cols-4 gap-4">
                                    <div class="text-center">
                                        <div class="text-3xl font-bold text-green-400">$10,000</div>
                                        <div class="text-xs text-gray-400">Monthly Revenue</div>
                                    </div>
                                    <div class="text-center">
                                        <div class="text-3xl font-bold text-blue-400">500</div>
                                        <div class="text-xs text-gray-400">Paying Users</div>
                                    </div>
                                    <div class="text-center">
                                        <div class="text-3xl font-bold text-orange-400">149</div>
                                        <div class="text-xs text-gray-400">Signups/Day</div>
                                    </div>
                                    <div class="text-center">
                                        <div class="text-3xl font-bold text-purple-400">41,670</div>
                                        <div class="text-xs text-gray-400">Website Visitors</div>
                                    </div>
                                </div>
                                <div class="mt-4 text-sm text-gray-400">
                                    User Mix: 270 Starter ($2,160) + 200 Pro ($6,000) + 20 Enterprise ($4,000) = $12,160 MRR
                                </div>
                            </div>
                        </div>
                    </div>

                    <!-- Top-Down vs Bottom-Up Funnels -->
                    <div x-show="selectedStrategy === 'funnels'" class="grid grid-cols-1 lg:grid-cols-2 gap-6">
                        <!-- Top-Down Funnel -->
                        <div class="bg-gray-800/30 rounded-lg p-6">
                            <h4 class="text-lg font-semibold mb-4 text-blue-400">📊 Top-Down (Market-Based)</h4>
                            <div class="space-y-4">
                                <div class="flex justify-between items-center">
                                    <span class="text-sm text-gray-400">Total Market (TAM)</span>
                                    <span class="font-semibold" x-text="(financialData?.growth_strategy?.top_down_funnel?.total_addressable_market || 0).toLocaleString()"></span>
                                </div>
                                <div class="w-full bg-gray-700 h-2 rounded-full">
                                    <div class="bg-blue-500 h-2 rounded-full" style="width: 100%"></div>
                                </div>
                                
                                <div class="flex justify-between items-center">
                                    <span class="text-sm text-gray-400">Realistic Reach (10%)</span>
                                    <span class="font-semibold" x-text="(financialData?.growth_strategy?.top_down_funnel?.realistic_reach_year_1 || 0).toLocaleString()"></span>
                                </div>
                                <div class="w-full bg-gray-700 h-2 rounded-full">
                                    <div class="bg-green-500 h-2 rounded-full" style="width: 80%"></div>
                                </div>
                                
                                <div class="flex justify-between items-center">
                                    <span class="text-sm text-gray-400">Website Visitors (30%)</span>
                                    <span class="font-semibold" x-text="(financialData?.growth_strategy?.top_down_funnel?.website_visitors_year_1 || 0).toLocaleString()"></span>
                                </div>
                                <div class="w-full bg-gray-700 h-2 rounded-full">
                                    <div class="bg-yellow-500 h-2 rounded-full" style="width: 60%"></div>
                                </div>
                                
                                <div class="flex justify-between items-center">
                                    <span class="text-sm text-gray-400">Signups (50%)</span>
                                    <span class="font-semibold" x-text="(financialData?.growth_strategy?.top_down_funnel?.signups_year_1 || 0).toLocaleString()"></span>
                                </div>
                                <div class="w-full bg-gray-700 h-2 rounded-full">
                                    <div class="bg-orange-500 h-2 rounded-full" style="width: 40%"></div>
                                </div>
                                
                                <div class="flex justify-between items-center">
                                    <span class="text-sm text-gray-400">Paying Customers (12%)</span>
                                    <span class="font-semibold text-green-400" x-text="(financialData?.growth_strategy?.top_down_funnel?.paying_customers_year_1 || 0).toLocaleString()"></span>
                                </div>
                                <div class="w-full bg-gray-700 h-2 rounded-full">
                                    <div class="bg-purple-500 h-2 rounded-full" style="width: 20%"></div>
                                </div>
                                
                                <div class="mt-4 pt-4 border-t border-gray-700">
                                    <div class="flex justify-between items-center">
                                        <span class="text-sm font-semibold">Year 1 Revenue</span>
                                        <span class="text-xl font-bold text-green-400" x-text="'$' + (financialData?.growth_strategy?.top_down_funnel?.annual_revenue_year_1 || 0).toLocaleString()"></span>
                                    </div>
                                </div>
                            </div>
                        </div>

                        <!-- Bottom-Up Funnel -->
                        <div class="bg-gray-800/30 rounded-lg p-6">
                            <h4 class="text-lg font-semibold mb-4 text-purple-400">🎯 Bottom-Up (User-Based)</h4>
                            <div class="space-y-4">
                                <div class="flex justify-between items-center">
                                    <span class="text-sm text-gray-400">Month 1 Target</span>
                                    <span class="font-semibold" x-text="(financialData?.growth_strategy?.bottom_up_funnel?.target_month_1 || 0) + ' users'"></span>
                                </div>
                                <div class="flex justify-between items-center text-green-400">
                                    <span class="text-xs">Revenue:</span>
                                    <span class="font-semibold" x-text="'$' + (financialData?.growth_strategy?.bottom_up_funnel?.month_1_revenue || 0).toLocaleString()"></span>
                                </div>
                                
                                <div class="flex justify-between items-center">
                                    <span class="text-sm text-gray-400">Month 2 Target</span>
                                    <span class="font-semibold" x-text="(financialData?.growth_strategy?.bottom_up_funnel?.target_month_2 || 0) + ' users'"></span>
                                </div>
                                <div class="flex justify-between items-center text-green-400">
                                    <span class="text-xs">Revenue:</span>
                                    <span class="font-semibold" x-text="'$' + (financialData?.growth_strategy?.bottom_up_funnel?.month_2_revenue || 0).toLocaleString()"></span>
                                </div>
                                
                                <div class="flex justify-between items-center">
                                    <span class="text-sm text-gray-400">Month 3 Target</span>
                                    <span class="font-semibold" x-text="(financialData?.growth_strategy?.bottom_up_funnel?.target_month_3 || 0) + ' users'"></span>
                                </div>
                                <div class="flex justify-between items-center text-green-400">
                                    <span class="text-xs">Revenue:</span>
                                    <span class="font-semibold" x-text="'$' + (financialData?.growth_strategy?.bottom_up_funnel?.month_3_revenue || 0).toLocaleString()"></span>
                                </div>
                                
                                <div class="flex justify-between items-center">
                                    <span class="text-sm text-gray-400">Month 6 Target</span>
                                    <span class="font-semibold" x-text="(financialData?.growth_strategy?.bottom_up_funnel?.target_month_6 || 0) + ' users'"></span>
                                </div>
                                <div class="flex justify-between items-center text-green-400">
                                    <span class="text-xs">Revenue:</span>
                                    <span class="font-semibold" x-text="'$' + (financialData?.growth_strategy?.bottom_up_funnel?.month_6_revenue || 0).toLocaleString()"></span>
                                </div>
                                
                                <div class="flex justify-between items-center">
                                    <span class="text-sm text-gray-400">Month 12 Target</span>
                                    <span class="font-semibold text-purple-400" x-text="(financialData?.growth_strategy?.bottom_up_funnel?.target_month_12 || 0) + ' users'"></span>
                                </div>
                                <div class="flex justify-between items-center text-green-400">
                                    <span class="text-xs">Revenue:</span>
                                    <span class="font-semibold text-lg" x-text="'$' + (financialData?.growth_strategy?.bottom_up_funnel?.month_12_revenue || 0).toLocaleString()"></span>
                                </div>
                                
                                <div class="mt-4 pt-4 border-t border-gray-700">
                                    <div class="text-center">
                                        <div class="text-xs text-gray-400 mb-1">Revenue Per User (Monthly)</div>
                                        <div class="text-2xl font-bold text-purple-400" x-text="'$' + (financialData?.growth_strategy?.bottom_up_funnel?.revenue_per_user_monthly || 0)"></div>
                                    </div>
                                </div>
                            </div>
                        </div>
                    </div>

                    <!-- Key Actions -->
                    <div class="mt-6 bg-purple-500/10 border border-purple-500/30 rounded-lg p-4">
                        <h4 class="text-sm font-semibold mb-3 text-purple-400">🎯 Key Actions This Month</h4>
                        <ul class="space-y-2">
                            <template x-for="action in financialData?.kpi_dashboard?.key_actions || []" :key="action">
                                <li class="flex items-center text-sm">
                                    <i class="fas fa-check-circle text-purple-400 mr-2"></i>
                                    <span x-text="action"></span>
                                </li>
                            </template>
                        </ul>
                    </div>
                </div>

                <!-- 5-Year Revenue Projections -->
                <div class="card-dark rounded-xl p-6" x-show="financialData">
                    <h3 class="text-xl font-bold mb-6">5-Year Revenue Projections</h3>
                    
                    <!-- Scenario Tabs -->
                    <div class="flex space-x-4 mb-6">
                        <button @click="selectedScenario = 'moderate_scenario'" 
                                :class="selectedScenario === 'moderate_scenario' ? 'bg-blue-600' : 'bg-gray-700'"
                                class="px-4 py-2 rounded text-sm font-medium">
                            Moderate
                        </button>
                        <button @click="selectedScenario = 'aggressive_scenario'" 
                                :class="selectedScenario === 'aggressive_scenario' ? 'bg-green-600' : 'bg-gray-700'"
                                class="px-4 py-2 rounded text-sm font-medium">
                            Aggressive
                        </button>
                        <button @click="selectedScenario = 'conservative_scenario'" 
                                :class="selectedScenario === 'conservative_scenario' ? 'bg-yellow-600' : 'bg-gray-700'"
                                class="px-4 py-2 rounded text-sm font-medium">
                            Conservative
                        </button>
                    </div>

                    <!-- Revenue Chart -->
                    <div class="h-64 mb-6">
                        <canvas id="revenueProjectionChart"></canvas>
                    </div>

                    <!-- Year 5 Projections Summary -->
                    <div class="grid grid-cols-1 md:grid-cols-4 gap-4">
                        <template x-if="getSelectedProjection()">
                            <div>
                                <div class="bg-gray-800/50 rounded-lg p-4 text-center">
                                    <p class="text-xs text-gray-400">Year 5 Revenue</p>
                                    <p class="text-xl font-bold text-green-400" x-text="formatCurrency(getSelectedProjection()?.total_revenue || 0)"></p>
                                </div>
                            </div>
                        </template>
                        <template x-if="getSelectedProjection()">
                            <div>
                                <div class="bg-gray-800/50 rounded-lg p-4 text-center">
                                    <p class="text-xs text-gray-400">Total Users</p>
                                    <p class="text-xl font-bold text-blue-400" x-text="(getSelectedProjection()?.total_users || 0).toLocaleString()"></p>
                                </div>
                            </div>
                        </template>
                        <template x-if="getSelectedProjection()">
                            <div>
                                <div class="bg-gray-800/50 rounded-lg p-4 text-center">
                                    <p class="text-xs text-gray-400">ARPU</p>
                                    <p class="text-xl font-bold text-purple-400" x-text="'$' + Math.round(getSelectedProjection()?.arpu || 0)"></p>
                                </div>
                            </div>
                        </template>
                        <div class="bg-gray-800/50 rounded-lg p-4 text-center">
                            <p class="text-xs text-gray-400">Market Share</p>
                            <p class="text-xl font-bold text-orange-400" x-text="calculateMarketShare() + '%'"></p>
                        </div>
                    </div>
                </div>

                <!-- Market Analysis & Unit Economics -->
                <div class="grid grid-cols-1 lg:grid-cols-2 gap-6" x-show="financialData">
                    <!-- LTV/CAC Analysis -->
                    <div class="card-dark rounded-xl p-6">
                        <h3 class="text-lg font-semibold mb-4 flex items-center">
                            <i class="fas fa-calculator text-green-400 mr-2"></i>
                            Unit Economics
                        </h3>
                        <div class="space-y-4">
                            <template x-for="(tier, tierName) in financialData?.unit_economics || {}" :key="tierName">
                                <div class="bg-gray-800/50 rounded-lg p-4">
                                    <div class="flex items-center justify-between mb-2">
                                        <span class="font-medium capitalize" x-text="tierName.replace('_tier', '')"></span>
                                        <span class="text-sm" :class="getLTVCACColor(tier.ltv, tier.cac)" x-text="'LTV:CAC ' + tier.ltv_cac_ratio.toFixed(1) + ':1'"></span>
                                    </div>
                                    <div class="grid grid-cols-4 gap-4 text-sm">
                                        <div>
                                            <p class="text-gray-400">Price</p>
                                            <p class="font-semibold text-green-400" x-text="'$' + tier.price"></p>
                                        </div>
                                        <div>
                                            <p class="text-gray-400">LTV</p>
                                            <p class="font-semibold" x-text="'$' + tier.ltv.toLocaleString()"></p>
                                        </div>
                                        <div>
                                            <p class="text-gray-400">CAC</p>
                                            <p class="font-semibold" x-text="'$' + tier.cac"></p>
                                        </div>
                                        <div>
                                            <p class="text-gray-400">Payback</p>
                                            <p class="font-semibold" x-text="tier.payback_months + ' mo'"></p>
                                        </div>
                                    </div>
                                </div>
                            </template>
                        </div>
                    </div>

                    <!-- Willingness to Pay -->
                    <div class="card-dark rounded-xl p-6">
                        <h3 class="text-lg font-semibold mb-4 flex items-center">
                            <i class="fas fa-users text-blue-400 mr-2"></i>
                            Willingness to Pay
                        </h3>
                        <div class="space-y-4">
                            <div class="bg-gray-800/50 rounded-lg p-4">
                                <h4 class="font-medium mb-3">Survey Data</h4>
                                <div class="text-sm text-gray-400">
                                    <p>Sample: <span class="text-white" x-text="financialData?.willingness_to_pay_analysis?.survey_data?.sample_size || 0"></span> respondents</p>
                                    <p>Method: <span class="text-white" x-text="financialData?.willingness_to_pay_analysis?.survey_data?.methodology || 'N/A'"></span></p>
                                </div>
                            </div>
                            <template x-for="(segment, segmentName) in financialData?.willingness_to_pay_analysis?.segment_willingness || {}" :key="segmentName">
                                <div class="bg-gray-800/50 rounded-lg p-4">
                                    <h4 class="font-medium mb-3 capitalize" x-text="segmentName"></h4>
                                    <div class="space-y-2 text-sm">
                                        <div class="flex justify-between">
                                            <span class="text-gray-400">Minimum:</span>
                                            <span class="text-red-400" x-text="'$' + segment.min"></span>
                                        </div>
                                        <div class="flex justify-between">
                                            <span class="text-gray-400">Optimal:</span>
                                            <span class="text-green-400 font-bold" x-text="'$' + segment.optimal"></span>
                                        </div>
                                        <div class="flex justify-between">
                                            <span class="text-gray-400">Maximum:</span>
                                            <span class="text-yellow-400" x-text="'$' + segment.max"></span>
                                        </div>
                                    </div>
                                </div>
                            </template>
                        </div>
                    </div>
                </div>

                <!-- Market Segments Analysis -->
                <div class="card-dark rounded-xl p-6" x-show="financialData">
                    <h3 class="text-lg font-semibold mb-4 flex items-center">
                        <i class="fas fa-chart-pie text-purple-400 mr-2"></i>
                        Market Segments & Opportunity
                    </h3>
                    <div class="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-4">
                        <template x-for="(segment, segmentName) in financialData?.market_segments || {}" :key="segmentName">
                            <div class="bg-gray-800/50 rounded-lg p-4">
                                <h4 class="font-medium text-sm mb-2 capitalize" x-text="segmentName.replace('_', ' ')"></h4>
                                <div class="space-y-2 text-xs">
                                    <div class="flex justify-between">
                                        <span class="text-gray-400">Size:</span>
                                        <span x-text="(segment.size / 1000).toFixed(1) + 'K'"></span>
                                    </div>
                                    <div class="flex justify-between">
                                        <span class="text-gray-400">WTP:</span>
                                        <span class="text-green-400 font-semibold" x-text="'$' + segment.willingness_to_pay"></span>
                                    </div>
                                    <div class="flex justify-between">
                                        <span class="text-gray-400">Target Tier:</span>
                                        <span class="capitalize" x-text="segment.target_tier"></span>
                                    </div>
                                    <div class="flex justify-between">
                                        <span class="text-gray-400">Pain Score:</span>
                                        <span :class="segment.pain_score > 85 ? 'text-red-400' : 'text-yellow-400'" x-text="segment.pain_score + '/100'"></span>
                                    </div>
                                    <div class="flex justify-between">
                                        <span class="text-gray-400">Difficulty:</span>
                                        <span class="capitalize" x-text="segment.acquisition_difficulty"></span>
                                    </div>
                                </div>
                            </div>
                        </template>
                    </div>
                </div>

                <!-- Competitor Benchmarks -->
                <div class="card-dark rounded-xl p-6" x-show="financialData">
                    <h3 class="text-lg font-semibold mb-4 flex items-center">
                        <i class="fas fa-trophy text-yellow-400 mr-2"></i>
                        Competitor Benchmarks
                    </h3>
                    <div class="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-4">
                        <template x-for="(data, competitor) in financialData?.competitive_benchmarks || {}" :key="competitor">
                            <div class="bg-gray-800/50 rounded-lg p-4" x-show="competitor !== 'zenyai_positioning'">
                                <h4 class="font-medium mb-3 capitalize" x-text="competitor"></h4>
                                <div class="space-y-2 text-sm">
                                    <div class="flex justify-between">
                                        <span class="text-gray-400">Price:</span>
                                        <span class="text-green-400" x-text="'$' + data.pricing"></span>
                                    </div>
                                    <div class="flex justify-between">
                                        <span class="text-gray-400">Users:</span>
                                        <span x-text="(data.users / 1000000).toFixed(1) + 'M'"></span>
                                    </div>
                                    <div class="flex justify-between">
                                        <span class="text-gray-400">Revenue:</span>
                                        <span x-text="'$' + (data.revenue_estimate / 1000000).toFixed(0) + 'M'"></span>
                                    </div>
                                    <div class="mt-2 pt-2 border-t border-gray-700">
                                        <p class="text-xs text-gray-400 mb-1">Strengths:</p>
                                        <template x-for="strength in data.strengths" :key="strength">
                                            <p class="text-xs text-green-400">✓ <span x-text="strength"></span></p>
                                        </template>
                                        <p class="text-xs text-gray-400 mb-1 mt-2">Weaknesses:</p>
                                        <template x-for="weakness in data.weaknesses" :key="weakness">
                                            <p class="text-xs text-red-400">✗ <span x-text="weakness"></span></p>
                                        </template>
                                    </div>
                                </div>
                            </div>
                        </template>
                        
                        <!-- Zenyai Positioning -->
                        <div class="bg-purple-500/20 rounded-lg p-4 border-2 border-purple-500">
                            <h4 class="font-medium mb-3 text-purple-400">Zenyai (You)</h4>
                            <div class="space-y-2 text-sm">
                                <div class="flex justify-between">
                                    <span class="text-gray-400">Price:</span>
                                    <span class="text-green-400 font-bold" x-text="financialData?.competitive_benchmarks?.zenyai_positioning?.pricing || '$8-200'"></span>
                                </div>
                                <div class="mt-2 pt-2 border-t border-purple-500/30">
                                    <p class="text-xs text-gray-400 mb-1">Unique Value:</p>
                                    <p class="text-xs text-white" x-text="financialData?.competitive_benchmarks?.zenyai_positioning?.unique_value"></p>
                                    <p class="text-xs text-gray-400 mb-1 mt-2">Advantages:</p>
                                    <template x-for="advantage in financialData?.competitive_benchmarks?.zenyai_positioning?.competitive_advantage || []" :key="advantage">
                                        <p class="text-xs text-green-400">✓ <span x-text="advantage"></span></p>
                                    </template>
                                </div>
                            </div>
                        </div>
                    </div>
                </div>

                <!-- Loading State -->
                <div x-show="!financialData" class="card-dark rounded-xl p-8 text-center">
                    <i class="fas fa-chart-line text-gray-400 text-4xl mb-4"></i>
                    <h3 class="text-lg font-semibold text-gray-300 mb-2">Financial Intelligence Dashboard</h3>
                    <p class="text-gray-400 mb-4">Comprehensive 5-year projections with market analysis</p>
                    <button @click="loadFinancialIntelligence()" class="bg-green-600 hover:bg-green-700 text-white px-6 py-2 rounded">
                        <i class="fas fa-chart-line mr-2"></i>
                        Load Financial Intelligence
                    </button>
                </div>
            </div>

            <!-- Marketing Videos View -->
            <div x-show="currentView === 'marketing-videos'" class="space-y-6">
                <div class="card-dark rounded-xl p-4 flex items-center justify-between">
                    <div>
                        <h3 class="text-lg font-bold">Viral Marketing Video Generator</h3>
                        <p class="text-xs text-gray-400">AI-powered video concepts based on real pain points</p>
                    </div>
                    <button @click="generateVideoConcepts()" class="bg-purple-600 hover:bg-purple-700 text-white text-sm px-3 py-2 rounded">
                        <i class="fas fa-video mr-1"></i>
                        Generate Concepts
                    </button>
                </div>

                <!-- Video Concepts -->
                <div class="space-y-6" x-show="videoConcepts && videoConcepts.length > 0">
                    <template x-for="(concept, index) in videoConcepts" :key="concept.id">
                        <div class="card-dark rounded-xl p-6 border border-purple-500/30">
                            <!-- Concept Header -->
                            <div class="flex items-start justify-between mb-4">
                                <div class="flex-1">
                                    <div class="flex items-center gap-2 mb-2">
                                        <span class="bg-purple-600 text-white text-xs px-2 py-1 rounded" x-text="'Concept ' + (index + 1)"></span>
                                        <span class="text-xs" :class="concept.estimated_engagement.viral_potential === 'High' ? 'text-green-400' : concept.estimated_engagement.viral_potential === 'Medium' ? 'text-yellow-400' : 'text-red-400'" x-text="concept.estimated_engagement.viral_potential + ' Viral Potential'"></span>
                                    </div>
                                    <h4 class="text-lg font-semibold mb-2" x-text="concept.hook"></h4>
                                    <p class="text-gray-400 text-sm mb-3" x-text="concept.scenario"></p>
                                    
                                    <!-- Concept Details -->
                                    <div class="grid grid-cols-2 md:grid-cols-4 gap-4 mb-4">
                                        <div class="bg-gray-800/50 rounded p-3 text-center">
                                            <p class="text-xs text-gray-400">Format</p>
                                            <p class="text-sm font-medium" x-text="concept.format.name"></p>
                                        </div>
                                        <div class="bg-gray-800/50 rounded p-3 text-center">
                                            <p class="text-xs text-gray-400">Duration</p>
                                            <p class="text-sm font-medium" x-text="concept.format.duration"></p>
                                        </div>
                                        <div class="bg-gray-800/50 rounded p-3 text-center">
                                            <p class="text-xs text-gray-400">Est. Views</p>
                                            <p class="text-sm font-medium" x-text="(concept.estimated_engagement && concept.estimated_engagement.estimated_views != null) ? concept.estimated_engagement.estimated_views.toLocaleString() : '—'"></p>
                                        </div>
                                        <div class="bg-gray-800/50 rounded p-3 text-center">
                                            <p class="text-xs text-gray-400">Engagement</p>
                                            <p class="text-sm font-medium" x-text="(concept.estimated_engagement && concept.estimated_engagement.engagement_rate != null) ? (concept.estimated_engagement.engagement_rate + '%') : '—'"></p>
                                        </div>
                                    </div>

                                    <!-- Visual Metaphor -->
                                    <div class="bg-gray-800/30 rounded p-3 mb-4">
                                        <p class="text-xs text-gray-400 mb-1">Visual Metaphor:</p>
                                        <p class="text-sm" x-text="concept.visual_metaphor"></p>
                                    </div>
                                </div>
                                
                                <!-- Regenerate Button -->
                                <button @click="regenerateConcept(concept.id, concept.pain_point_category)" 
                                        class="bg-gray-700 hover:bg-gray-600 text-white text-sm px-3 py-2 rounded ml-4">
                                    <i class="fas fa-sync-alt mr-1"></i>
                                    Regenerate
                                </button>
                            </div>

                            <!-- Video Prompts -->
                            <div class="grid grid-cols-1 lg:grid-cols-2 gap-4 mb-6">
                                <!-- Sora Prompt -->
                                <div class="bg-gray-800/50 rounded-lg p-4">
                                    <div class="flex items-center justify-between mb-2">
                                        <h5 class="font-medium text-blue-400">Sora Prompt</h5>
                                        <button @click="copyToClipboard(concept.sora_prompt)" class="text-xs text-gray-400 hover:text-white">
                                            <i class="fas fa-copy mr-1"></i>Copy
                                        </button>
                                    </div>
                                    <p class="text-sm text-gray-300 mb-3 max-h-24 overflow-y-auto" x-text="concept.sora_prompt"></p>
                                    <button @click="generateSoraVideo(concept)" 
                                            type="button"
                                            class="w-full bg-blue-600 hover:bg-blue-700 text-white text-sm py-2 rounded transition-all pointer-events-auto relative z-10">
                                        <span x-show="concept.generating_sora"><i class="fas fa-spinner fa-spin mr-2"></i>Generating Video...</span>
                                        <span x-show="!concept.generating_sora && !concept.sora_video"><i class="fas fa-play mr-2"></i>Generate Sora</span>
                                        <span x-show="!concept.generating_sora && concept.sora_video"><i class="fas fa-check mr-2"></i>Generated!</span>
                                    </button>
                                </div>

                                <!-- Gemini Prompt -->
                                <div class="bg-gray-800/50 rounded-lg p-4">
                                    <div class="flex items-center justify-between mb-2">
                                        <h5 class="font-medium text-green-400">Gemini Prompt</h5>
                                        <button @click="copyToClipboard(concept.gemini_prompt)" class="text-xs text-gray-400 hover:text-white">
                                            <i class="fas fa-copy mr-1"></i>Copy
                                        </button>
                                    </div>
                                    <p class="text-sm text-gray-300 mb-3 max-h-24 overflow-y-auto" x-text="concept.gemini_prompt"></p>
                                    <button @click="generateGeminiVideo(concept)" 
                                            type="button"
                                            class="w-full bg-green-600 hover:bg-green-700 text-white text-sm py-2 rounded transition-all pointer-events-auto relative z-10">
                                        <span x-show="concept.generating_gemini"><i class="fas fa-spinner fa-spin mr-2"></i>Generating Video...</span>
                                        <span x-show="!concept.generating_gemini && !concept.gemini_video"><i class="fas fa-play mr-2"></i>Generate Gemini</span>
                                        <span x-show="!concept.generating_gemini && concept.gemini_video"><i class="fas fa-check mr-2"></i>Generated!</span>
                                    </button>
                                </div>
                            </div>

                            <!-- Generated Videos -->
                            <div x-show="concept.sora_video || concept.gemini_video" class="border-t border-gray-700 pt-4">
                                <h5 class="font-medium mb-3">Generated Videos</h5>
                                <div class="grid grid-cols-1 md:grid-cols-2 gap-4">
                                    <!-- Sora Video -->
                                    <template x-if="concept.sora_video">
                                        <div class="bg-gray-800/30 rounded-lg p-4">
                                            <div class="flex items-center justify-between mb-2">
                                                <span class="text-sm font-medium text-blue-400">Sora Video</span>
                                                <span class="text-xs text-gray-400" x-text="concept.sora_video.file_size"></span>
                                            </div>
                                            <div class="bg-gray-700 rounded h-32 mb-3 flex items-center justify-center">
                                                <i class="fas fa-play-circle text-3xl text-blue-400"></i>
                                            </div>
                                            <div class="flex gap-2">
                                                <button @click="previewVideo(concept.sora_video)" class="flex-1 bg-blue-600 hover:bg-blue-700 text-white text-xs py-2 rounded">
                                                    <i class="fas fa-play mr-1"></i>Preview
                                                </button>
                                                <button @click="downloadVideo(concept.sora_video)" class="flex-1 bg-gray-600 hover:bg-gray-700 text-white text-xs py-2 rounded">
                                                    <i class="fas fa-download mr-1"></i>Download
                                                </button>
                                            </div>
                                        </div>
                                    </template>

                                    <!-- Gemini Video -->
                                    <template x-if="concept.gemini_video">
                                        <div class="bg-gray-800/30 rounded-lg p-4">
                                            <div class="flex items-center justify-between mb-2">
                                                <span class="text-sm font-medium text-green-400">Gemini Video</span>
                                                <span class="text-xs text-gray-400" x-text="concept.gemini_video.file_size"></span>
                                            </div>
                                            <div class="bg-gray-700 rounded h-32 mb-3 flex items-center justify-center">
                                                <i class="fas fa-play-circle text-3xl text-green-400"></i>
                                            </div>
                                            <div class="flex gap-2">
                                                <button @click="previewVideo(concept.gemini_video)" class="flex-1 bg-green-600 hover:bg-green-700 text-white text-xs py-2 rounded">
                                                    <i class="fas fa-play mr-1"></i>Preview
                                                </button>
                                                <button @click="downloadVideo(concept.gemini_video)" class="flex-1 bg-gray-600 hover:bg-gray-700 text-white text-xs py-2 rounded">
                                                    <i class="fas fa-download mr-1"></i>Download
                                                </button>
                                            </div>
                                        </div>
                                    </template>
                                </div>
                            </div>

                            <!-- Platforms -->
                            <div class="flex items-center gap-2 mt-4">
                                <span class="text-xs text-gray-400">Platforms:</span>
                                <template x-for="platform in concept.target_platforms" :key="platform">
                                    <span class="bg-purple-600/20 text-purple-400 text-xs px-2 py-1 rounded" x-text="platform"></span>
                                </template>
                            </div>
                        </div>
                    </template>
                </div>

                <!-- Loading State -->
                <div x-show="!videoConcepts || videoConcepts.length === 0" class="card-dark rounded-xl p-8 text-center">
                    <i class="fas fa-video text-gray-400 text-4xl mb-4"></i>
                    <h3 class="text-lg font-semibold text-gray-300 mb-2">Viral Video Generator</h3>
                    <p class="text-gray-400 mb-4">Generate AI-powered video concepts based on real pain points</p>
                    <button @click="generateVideoConcepts()" class="bg-purple-600 hover:bg-purple-700 text-white px-6 py-2 rounded">
                        <i class="fas fa-video mr-2"></i>
                        Generate Video Concepts
                    </button>
                </div>
            </div>

            <!-- Audio Intelligence View -->
            <div x-show="currentView === 'audio-intelligence'" class="space-y-6">
                <!-- Executive Summary -->
                <div class="card-dark rounded-xl p-6">
                    <div class="flex items-center justify-between mb-4">
                        <h3 class="text-xl font-bold text-white">Audio Industry Intelligence</h3>
                        <button @click="loadAudioIntelligence()" class="bg-purple-600 hover:bg-purple-700 text-white text-sm px-4 py-2 rounded">
                            <i class="fas fa-sync-alt mr-2"></i>Refresh Analysis
                        </button>
                    </div>
                    
                    <template x-if="audioIntelligence">
                        <div class="grid grid-cols-1 md:grid-cols-4 gap-4 mb-6">
                            <div class="bg-gradient-to-r from-purple-600/20 to-blue-600/20 rounded-lg p-4 border border-purple-500/30">
                                <div class="text-2xl font-bold text-purple-400" x-text="audioIntelligence.overall_opportunity_score.toFixed(1) + '/100'"></div>
                                <div class="text-sm text-gray-300">Opportunity Score</div>
                            </div>
                            <div class="bg-gradient-to-r from-green-600/20 to-emerald-600/20 rounded-lg p-4 border border-green-500/30">
                                <div class="text-2xl font-bold text-green-400">92.0/100</div>
                                <div class="text-sm text-gray-300">Zenyai Pain Score</div>
                            </div>
                            <div class="bg-gradient-to-r from-blue-600/20 to-cyan-600/20 rounded-lg p-4 border border-blue-500/30">
                                <div class="text-2xl font-bold text-blue-400">$11.9B</div>
                                <div class="text-sm text-gray-300">Total Market</div>
                            </div>
                            <div class="bg-gradient-to-r from-orange-600/20 to-red-600/20 rounded-lg p-4 border border-orange-500/30">
                                <div class="text-2xl font-bold text-orange-400">#1</div>
                                <div class="text-sm text-gray-300">Market Position</div>
                            </div>
                        </div>
                    </template>

                    <!-- Executive Summary -->
                    <template x-if="audioIntelligence && audioIntelligence.executive_summary">
                        <div class="bg-gray-800/50 rounded-lg p-4 mb-6">
                            <h4 class="font-semibold text-white mb-3">Executive Summary</h4>
                            <div class="space-y-2 text-sm text-gray-300">
                                <p><strong class="text-purple-400">Market Validation:</strong> <span x-text="audioIntelligence.executive_summary.market_validation"></span></p>
                                <p><strong class="text-blue-400">Competitive Position:</strong> <span x-text="audioIntelligence.executive_summary.competitive_position"></span></p>
                                <p><strong class="text-green-400">Recommendation:</strong> <span x-text="audioIntelligence.executive_summary.recommendation"></span></p>
                                <p><strong class="text-orange-400">Next Expansion:</strong> <span x-text="audioIntelligence.executive_summary.next_expansion"></span></p>
                            </div>
                        </div>
                    </template>
                </div>

                <!-- Pain Points Analysis -->
                <template x-if="audioIntelligence && audioIntelligence.pain_points">
                    <div class="card-dark rounded-xl p-6">
                        <h3 class="text-xl font-bold text-white mb-4">Audio Industry Pain Points</h3>
                        <div class="grid grid-cols-1 lg:grid-cols-2 gap-4">
                            <template x-for="painPoint in audioIntelligence.pain_points.slice(0, 6)" :key="painPoint.description">
                                <div class="bg-gray-800/50 rounded-lg p-4 border-l-4" 
                                     :class="painPoint.severity_score >= 90 ? 'border-red-500' : painPoint.severity_score >= 85 ? 'border-orange-500' : 'border-yellow-500'">
                                    <div class="flex items-center justify-between mb-2">
                                        <span class="text-xs font-medium px-2 py-1 rounded" 
                                              :class="painPoint.industry === 'universal' ? 'bg-purple-600/20 text-purple-400' : 
                                                     painPoint.industry === 'gaming' ? 'bg-blue-600/20 text-blue-400' :
                                                     painPoint.industry === 'film' ? 'bg-green-600/20 text-green-400' :
                                                     'bg-orange-600/20 text-orange-400'"
                                              x-text="painPoint.industry.charAt(0).toUpperCase() + painPoint.industry.slice(1)"></span>
                                        <span class="text-lg font-bold" 
                                              :class="painPoint.severity_score >= 90 ? 'text-red-400' : painPoint.severity_score >= 85 ? 'text-orange-400' : 'text-yellow-400'"
                                              x-text="painPoint.severity_score.toFixed(1)"></span>
                                    </div>
                                    <p class="text-sm text-gray-300 mb-2" x-text="painPoint.description"></p>
                                    <div class="text-xs text-gray-400">
                                        <span>Frequency: </span><span x-text="painPoint.frequency"></span>
                                        <span class="ml-4">Gap Score: </span><span x-text="painPoint.market_gap_score.toFixed(1)"></span>
                                    </div>
                                </div>
                            </template>
                        </div>
                    </div>
                </template>

                <!-- Market Opportunities -->
                <template x-if="audioIntelligence && audioIntelligence.market_opportunities">
                    <div class="card-dark rounded-xl p-6">
                        <h3 class="text-xl font-bold text-white mb-4">Market Opportunities</h3>
                        <div class="grid grid-cols-1 md:grid-cols-2 gap-6">
                            <!-- TAM Analysis -->
                            <div class="bg-gray-800/50 rounded-lg p-4">
                                <h4 class="font-semibold text-blue-400 mb-3">Total Addressable Market</h4>
                                <template x-if="audioIntelligence.market_opportunities.tam_analysis">
                                    <div class="space-y-2 text-sm">
                                        <div class="flex justify-between">
                                            <span class="text-gray-300">Gaming Audio:</span>
                                            <span class="text-white font-medium">$2.8B</span>
                                        </div>
                                        <div class="flex justify-between">
                                            <span class="text-gray-300">Film Audio:</span>
                                            <span class="text-white font-medium">$4.2B</span>
                                        </div>
                                        <div class="flex justify-between">
                                            <span class="text-gray-300">Podcast Market:</span>
                                            <span class="text-white font-medium">$1.8B</span>
                                        </div>
                                        <div class="flex justify-between border-t border-gray-600 pt-2">
                                            <span class="text-blue-400 font-medium">Total TAM:</span>
                                            <span class="text-blue-400 font-bold">$11.9B</span>
                                        </div>
                                    </div>
                                </template>
                            </div>

                            <!-- Zenyai Validation -->
                            <div class="bg-gray-800/50 rounded-lg p-4">
                                <h4 class="font-semibold text-green-400 mb-3">Zenyai Market Validation</h4>
                                <template x-if="audioIntelligence.market_opportunities.zenyai_target_validation">
                                    <div class="space-y-2 text-sm">
                                        <div class="flex justify-between">
                                            <span class="text-gray-300">Pain Score:</span>
                                            <span class="text-green-400 font-bold">92.0/100</span>
                                        </div>
                                        <div class="text-gray-300 text-xs" x-text="audioIntelligence.market_opportunities.zenyai_target_validation.market_position"></div>
                                        <div class="bg-green-600/20 rounded p-2 mt-2">
                                            <div class="text-green-400 font-medium text-xs">Competitive Advantage:</div>
                                            <div class="text-green-300 text-xs" x-text="audioIntelligence.market_opportunities.zenyai_target_validation.competitive_advantage"></div>
                                        </div>
                                    </div>
                                </template>
                            </div>
                        </div>
                    </div>
                </template>

                <!-- Loading State -->
                <div x-show="!audioIntelligence" class="card-dark rounded-xl p-8 text-center">
                    <i class="fas fa-headphones text-gray-400 text-4xl mb-4"></i>
                    <h3 class="text-lg font-semibold text-gray-300 mb-2">Audio Industry Intelligence</h3>
                    <p class="text-gray-400 mb-4">Comprehensive analysis of audio professional pain points and market opportunities</p>
                    <button @click="loadAudioIntelligence()" class="bg-purple-600 hover:bg-purple-700 text-white px-6 py-2 rounded">
                        <i class="fas fa-chart-line mr-2"></i>
                        Run Audio Analysis
                    </button>
                </div>
            </div>

            <!-- Angel Investors View -->
            <div x-show="currentView === 'angel-investors'" class="space-y-6">
                <!-- Header & Filters -->
                <div class="card-dark rounded-xl p-6">
                    <div class="flex items-center justify-between mb-6">
                        <div>
                            <h3 class="text-2xl font-bold text-green-400">💰 Angel Investor Database</h3>
                            <p class="text-gray-400 text-sm">240 high-quality investors for Zenyai's AI-powered creative tools</p>
                        </div>
                        <div class="flex items-center space-x-4">
                            <button @click="debugMemoryStatus()" 
                                    class="bg-yellow-600 hover:bg-yellow-700 px-3 py-2 rounded-lg font-medium text-xs transition-colors">
                                🔍 Debug Memory
                            </button>
                            <button @click="bulkSendInvestorEmails()" 
                                    class="bg-green-600 hover:bg-green-700 px-4 py-2 rounded-lg font-medium text-sm transition-colors flex items-center space-x-2">
                                <i class="fas fa-paper-plane"></i>
                                <span x-text="'📧 Bulk Send Next 12 (' + (angelInvestors ? (Array.isArray(angelInvestors) ? angelInvestors : Object.values(angelInvestors)).filter(inv => !isInvestorContacted(inv.name)).length : 0) + ' uncontacted)'"></span>
                            </button>
                            <div class="text-right" x-show="angelInvestors">
                                <div class="text-3xl font-bold text-green-400" x-text="Object.keys(angelInvestors || {}).length"></div>
                                <div class="text-xs text-gray-400">Total Investors</div>
                            </div>
                        </div>
                    </div>

                    <!-- Category Filters -->
                    <div class="flex flex-wrap gap-2">
                        <button @click="loadAngelInvestors('all')" 
                                :class="selectedInvestorCategory === 'all' ? 'bg-green-600' : 'bg-gray-700'"
                                class="px-4 py-2 rounded text-sm font-medium hover:bg-green-700">
                            🌐 All Investors
                        </button>
                        <button @click="loadAngelInvestors('audio')" 
                                :class="selectedInvestorCategory === 'audio' ? 'bg-purple-600' : 'bg-gray-700'"
                                class="px-4 py-2 rounded text-sm font-medium hover:bg-purple-700">
                            🎵 Audio/Music Tech
                        </button>
                        <button @click="loadAngelInvestors('ai')" 
                                :class="selectedInvestorCategory === 'ai' ? 'bg-blue-600' : 'bg-gray-700'"
                                class="px-4 py-2 rounded text-sm font-medium hover:bg-blue-700">
                            🤖 AI/ML Experts
                        </button>
                        <button @click="loadAngelInvestors('saas')" 
                                :class="selectedInvestorCategory === 'saas' ? 'bg-orange-600' : 'bg-gray-700'"
                                class="px-4 py-2 rounded text-sm font-medium hover:bg-orange-700">
                            💼 SaaS Specialists
                        </button>
                        <button @click="loadAngelInvestors('creator')" 
                                :class="selectedInvestorCategory === 'creator' ? 'bg-pink-600' : 'bg-gray-700'"
                                class="px-4 py-2 rounded text-sm font-medium hover:bg-pink-700">
                            ✨ Creator Economy
                        </button>
                    </div>
                </div>

                <!-- Investor Cards Grid -->
                <div x-show="angelInvestors" class="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-4">
                    <template x-for="(investor, key) in angelInvestors" :key="key">
                        <div class="card-dark rounded-xl p-5 hover:border-green-500/50 border-2 border-gray-700 transition-all"
                             :class="isInvestorContacted(investor.name) ? 'opacity-60 bg-gray-800/50 border-green-500' : ''">
                            <!-- Header with Checkbox -->
                            <div class="flex items-start justify-between mb-3">
                                <div class="flex-1">
                                    <div class="flex items-center gap-3 mb-1">
                                        <input type="checkbox" 
                                               :checked="isInvestorContacted(investor.name)"
                                               @change="toggleInvestorContacted(investor.name)"
                                               class="w-5 h-5 rounded border-2 border-green-500 bg-gray-700 checked:bg-green-600 cursor-pointer">
                                        <h4 class="font-bold text-lg text-white" x-text="investor.name"
                                            :class="isInvestorContacted(investor.name) ? 'line-through text-gray-500' : ''"></h4>
                                    </div>
                                    <p class="text-xs text-gray-400 ml-8" x-text="investor.title"></p>
                                </div>
                                <div class="text-right">
                                    <div class="text-green-400 font-bold text-sm" x-text="investor.check_size"></div>
                                    <div class="text-xs text-gray-500">Check Size</div>
                                </div>
                            </div>

                            <!-- Focus Areas -->
                            <div class="mb-3">
                                <div class="flex flex-wrap gap-1">
                                    <template x-for="focus in investor.focus" :key="focus">
                                        <span class="px-2 py-1 bg-blue-500/20 text-blue-300 rounded text-xs" x-text="focus"></span>
                                    </template>
                                </div>
                            </div>

                            <!-- Why Zenyai -->
                            <div class="mb-3 p-3 bg-purple-500/10 rounded border-l-2 border-purple-500">
                                <div class="text-xs text-gray-400 mb-1">Why Zenyai:</div>
                                <div class="text-sm text-gray-200" x-text="investor.why_zenyai"></div>
                            </div>

                            <!-- Notable Investments -->
                            <div class="mb-3">
                                <div class="text-xs text-gray-400 mb-1">Notable Investments:</div>
                                <div class="text-xs text-gray-300">
                                    <template x-for="(investment, idx) in investor.notable_investments.slice(0, 3)" :key="idx">
                                        <span>
                                            <span x-text="investment"></span><span x-show="idx < 2">, </span>
                                        </span>
                                    </template>
                                </div>
                            </div>

                            <!-- Investment Pitch Email -->
                            <div class="mb-4 p-4 bg-gradient-to-r from-green-900/30 to-blue-900/30 rounded-lg border border-green-500/30">
                                <div class="flex items-center justify-between mb-3">
                                    <div class="flex items-center gap-2">
                                        <i class="fas fa-dollar-sign text-green-400"></i>
                                        <span class="text-xs font-semibold text-green-300 uppercase tracking-wide">Investment Pitch - Ready to Send</span>
                                    </div>
                                    <div class="flex gap-2">
                                        <button @click="regenerateInvestorEmail(investor)" 
                                                class="px-3 py-2 bg-blue-600 hover:bg-blue-500 text-white text-xs font-semibold rounded transition-all flex items-center gap-1">
                                            <i class="fas fa-sync-alt"></i> Regenerate
                                        </button>
                                        <button @click="copyInvestorPitch(investor)" 
                                                class="px-3 py-2 bg-gray-600 hover:bg-gray-500 text-white text-xs font-semibold rounded transition-all flex items-center gap-1">
                                            <i class="fas fa-copy"></i> Copy
                                        </button>
                                    </div>
                                </div>
                                <div class="max-h-64 overflow-y-auto pr-2 text-sm text-gray-200 leading-relaxed whitespace-pre-line font-mono bg-gray-900/50 p-3 rounded border border-gray-700" 
                                     x-text="generateInvestorPitch(investor)"></div>
                                
                                <!-- Send Email Buttons -->
                                <div class="mt-3 pt-3 border-t border-green-500/30 space-y-2">
                                    <!-- Test Email Button -->
                                    <button @click="sendTestInvestorEmail(investor)" 
                                            class="w-full py-2 bg-blue-600 hover:bg-blue-500 text-white text-xs font-semibold rounded-lg transition-all flex items-center justify-center gap-2">
                                        <i class="fas fa-vial"></i>
                                        <span>Send Test to MY Email First</span>
                                    </button>
                                    
                                    <!-- Real Send Button -->
                                    <button @click="sendEmailToInvestor(investor)" 
                                            :disabled="isInvestorContacted(investor.name)"
                                            :class="isInvestorContacted(investor.name) ? 'bg-gray-600 cursor-not-allowed opacity-50' : 'bg-green-600 hover:bg-green-500'"
                                            class="w-full py-3 text-white text-sm font-bold rounded-lg transition-all flex items-center justify-center gap-2 shadow-lg">
                                        <i :class="isInvestorContacted(investor.name) ? 'fas fa-check-circle' : 'fas fa-paper-plane'"></i>
                                        <span x-text="isInvestorContacted(investor.name) ? '✅ Email Already Sent' : '🚀 Send Pitch to ' + investor.name.split(' ')[0]"></span>
                                    </button>
                                </div>
                            </div>

                            <!-- Contact Info -->
                            <div class="border-t border-gray-700 pt-3 space-y-2">
                                <div class="flex items-center justify-between text-xs">
                                    <a :href="investor.linkedin" target="_blank" class="text-blue-400 hover:text-blue-300 flex items-center">
                                        <i class="fab fa-linkedin mr-1"></i>
                                        LinkedIn
                                    </a>
                                    <span class="text-purple-400" x-text="investor.twitter"></span>
                                </div>
                                <div class="text-xs text-gray-400">
                                    <i class="fas fa-envelope mr-1"></i>
                                    <span x-text="investor.contact_method"></span>
                                </div>
                            </div>
                        </div>
                    </template>
                </div>

                <!-- Loading State -->
                <div x-show="!angelInvestors" class="card-dark rounded-xl p-8 text-center">
                    <i class="fas fa-hand-holding-usd text-gray-400 text-4xl mb-4"></i>
                    <h3 class="text-lg font-semibold text-gray-300 mb-2">Angel Investor Database</h3>
                    <p class="text-gray-400 mb-4">60 curated investors perfect for Zenyai's Audio AI platform</p>
                    <button @click="loadAngelInvestors()" class="bg-green-600 hover:bg-green-700 text-white px-6 py-2 rounded">
                        <i class="fas fa-users mr-2"></i>
                        Load Investors
                    </button>
                </div>
            </div>

            <!-- Affiliate Partners View -->
            <div x-show="currentView === 'affiliate-partners'" class="space-y-6">
                <!-- Header & Filters -->
                <div class="card-dark rounded-xl p-6">
                    <div class="flex items-center justify-between mb-4">
                        <div>
                            <h3 class="text-2xl font-bold text-purple-400">🤝 Affiliate Partnership Database</h3>
                            <p class="text-gray-400 text-sm" x-show="affiliatePartners && affiliatePartners.length > 0">
                                <span x-text="affiliatePartners.length"></span> potential partners across Audio, Film, Podcast & Gaming
                            </p>
                            <p class="text-gray-400 text-sm" x-show="!affiliatePartners || affiliatePartners.length === 0">
                                Loading partners... Click a category button below to load
                            </p>
                        </div>
                        <div class="flex items-center space-x-4">
                            <button @click="debugMemoryStatus()" 
                                    class="bg-yellow-600 hover:bg-yellow-700 px-3 py-2 rounded-lg font-medium text-xs transition-colors">
                                🔍 Debug Memory
                            </button>
                            <button @click="bulkSendPartnerEmails()" 
                                    class="bg-purple-600 hover:bg-purple-700 px-4 py-2 rounded-lg font-medium text-sm transition-colors flex items-center space-x-2">
                                <i class="fas fa-paper-plane"></i>
                                <span x-text="'📧 Bulk Send Next 12 (' + (affiliatePartners ? affiliatePartners.filter(p => !isPartnerContacted(p.name)).length : 0) + ' uncontacted)'"></span>
                            </button>
                        </div>
                    </div>
                    
                    <!-- Category Filters -->
                    <div class="flex flex-wrap gap-2">
                        <button @click="loadAffiliatePartners('all')" 
                                :class="selectedAffiliateCategory === 'all' ? 'bg-purple-600' : 'bg-gray-700 hover:bg-gray-600'"
                                class="px-4 py-2 rounded text-sm text-white">
                            🌐 All (240)
                        </button>
                        <button @click="loadAffiliatePartners('audio')" 
                                :class="selectedAffiliateCategory === 'audio' ? 'bg-purple-600' : 'bg-gray-700 hover:bg-gray-600'"
                                class="px-4 py-2 rounded text-sm text-white">
                            🎵 Audio (60)
                        </button>
                        <button @click="loadAffiliatePartners('film')" 
                                :class="selectedAffiliateCategory === 'film' ? 'bg-purple-600' : 'bg-gray-700 hover:bg-gray-600'"
                                class="px-4 py-2 rounded text-sm text-white">
                            🎬 Film (60)
                        </button>
                        <button @click="loadAffiliatePartners('podcast')" 
                                :class="selectedAffiliateCategory === 'podcast' ? 'bg-purple-600' : 'bg-gray-700 hover:bg-gray-600'"
                                class="px-4 py-2 rounded text-sm text-white">
                            🎙️ Podcast (60)
                        </button>
                        <button @click="loadAffiliatePartners('gaming')" 
                                :class="selectedAffiliateCategory === 'gaming' ? 'bg-purple-600' : 'bg-gray-700 hover:bg-gray-600'"
                                class="px-4 py-2 rounded text-sm text-white">
                            🎮 Gaming (60)
                        </button>
                    </div>
                </div>

                <!-- Partners Grid -->
                <div x-show="affiliatePartners" class="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-4">
                    <template x-for="partner in affiliatePartners" :key="partner.id">
                        <div class="card-dark rounded-xl p-5 hover:border-purple-500 transition-all border-2 border-transparent"
                             :class="isPartnerContacted(partner.name) ? 'opacity-60 bg-gray-800/50' : ''">
                            <!-- Header with Checkbox -->
                            <div class="flex items-start justify-between mb-4">
                                <div class="flex-1">
                                    <div class="flex items-center gap-3 mb-1">
                                        <input type="checkbox" 
                                               :checked="isPartnerContacted(partner.name)"
                                               @change="togglePartnerContacted(partner.name)"
                                               class="w-5 h-5 rounded border-2 border-purple-500 bg-gray-700 checked:bg-purple-600 cursor-pointer">
                                        <h4 class="text-lg font-bold text-white" x-text="partner.name"
                                            :class="isPartnerContacted(partner.name) ? 'line-through text-gray-500' : ''"></h4>
                                    </div>
                                    <p class="text-xs text-gray-400 capitalize mb-2 ml-8">
                                        <i class="fas fa-play-circle mr-1"></i>
                                        <span x-text="partner.platform"></span> • <span x-text="partner.category"></span>
                                    </p>
                                    <span class="px-2 py-1 bg-green-500/20 text-green-300 rounded text-xs font-semibold ml-8">
                                        <i class="fas fa-users mr-1"></i><span x-text="partner.followers"></span>
                                    </span>
                                </div>
                            </div>
                            
                            <!-- Description -->
                            <div class="mb-3 text-sm text-gray-300" x-text="partner.description || partner.why"></div>
                            
                            <!-- Why Partner -->
                            <div class="mb-4 p-3 bg-purple-500/10 rounded border-l-2 border-purple-500">
                                <div class="text-xs text-gray-400 mb-1">Why Partner:</div>
                                <div class="text-sm text-gray-200" x-text="partner.why_partner || partner.why"></div>
                            </div>
                            
                            <!-- Outreach Message -->
                            <div class="mb-4 p-4 bg-gradient-to-r from-purple-900/30 to-blue-900/30 rounded-lg border border-purple-500/30">
                                <div class="flex items-center justify-between mb-3">
                                    <div class="flex items-center gap-2">
                                        <i class="fas fa-envelope text-purple-400"></i>
                                        <span class="text-xs font-semibold text-purple-300 uppercase tracking-wide">Email Template - Ready to Send</span>
                                    </div>
                                    <div class="flex gap-2">
                                        <button @click="regenerateEmailVariant(partner)" 
                                                class="px-3 py-2 bg-blue-600 hover:bg-blue-500 text-white text-xs font-semibold rounded transition-all flex items-center gap-1">
                                            <i class="fas fa-sync-alt"></i> Regenerate
                                        </button>
                                        <button @click="copyOutreachMessage(partner)" 
                                                class="px-3 py-2 bg-gray-600 hover:bg-gray-500 text-white text-xs font-semibold rounded transition-all flex items-center gap-1">
                                            <i class="fas fa-copy"></i> Copy
                                        </button>
                                    </div>
                                </div>
                                <div class="max-h-64 overflow-y-auto pr-2 text-sm text-gray-200 leading-relaxed whitespace-pre-line font-mono bg-gray-900/50 p-3 rounded border border-gray-700" 
                                     x-text="generateOutreachMessage(partner)"></div>
                                
                                <!-- Send Email Buttons -->
                                <div class="mt-3 pt-3 border-t border-purple-500/30 space-y-2">
                                    <!-- Test Email Button -->
                                    <button @click="sendTestEmailToMyself(partner)" 
                                            class="w-full py-2 bg-blue-600 hover:bg-blue-500 text-white text-xs font-semibold rounded-lg transition-all flex items-center justify-center gap-2">
                                        <i class="fas fa-vial"></i>
                                        <span>Send Test to MY Email First</span>
                                    </button>
                                    
                                    <!-- Real Send Button -->
                                    <button @click="sendEmailToPartner(partner)" 
                                            :disabled="isPartnerContacted(partner.name)"
                                            :class="isPartnerContacted(partner.name) ? 'bg-gray-600 cursor-not-allowed opacity-50' : 'bg-green-600 hover:bg-green-500'"
                                            class="w-full py-3 text-white text-sm font-bold rounded-lg transition-all flex items-center justify-center gap-2 shadow-lg">
                                        <i :class="isPartnerContacted(partner.name) ? 'fas fa-check-circle' : 'fas fa-paper-plane'"></i>
                                        <span x-text="isPartnerContacted(partner.name) ? '✅ Email Already Sent' : '🚀 Send Email to ' + partner.name.split(' ')[0]"></span>
                                    </button>
                                </div>
                            </div>
                            
                            <!-- Contact Links -->
                            <div class="border-t border-gray-700 pt-3 space-y-2">
                                <div class="flex items-center justify-between text-xs">
                                    <a x-show="partner.youtube" :href="partner.youtube" target="_blank" class="text-red-400 hover:text-red-300 flex items-center">
                                        <i class="fab fa-youtube mr-1"></i> YouTube
                                    </a>
                                    <a x-show="partner.twitter" :href="'https://twitter.com/' + partner.twitter.replace('@', '')" target="_blank" class="text-blue-400 hover:text-blue-300 flex items-center">
                                        <i class="fab fa-twitter mr-1"></i> Twitter
                                    </a>
                                    <a x-show="partner.website" :href="partner.website" target="_blank" class="text-purple-400 hover:text-purple-300 flex items-center">
                                        <i class="fas fa-globe mr-1"></i> Website
                                    </a>
                                </div>
                                <div x-show="partner.email" class="text-xs">
                                    <span class="text-gray-400">Email:</span>
                                    <a :href="'mailto:' + partner.email" class="text-green-400 hover:text-green-300 ml-2" x-text="partner.email"></a>
                                </div>
                            </div>
                        </div>
                    </template>
                </div>

                <!-- Loading State -->
                <div x-show="!affiliatePartners" class="card-dark rounded-xl p-8 text-center">
                    <i class="fas fa-handshake text-gray-400 text-4xl mb-4"></i>
                    <h3 class="text-lg font-semibold text-gray-300 mb-2">Affiliate Partnership Database</h3>
                    <p class="text-gray-400 mb-4">60 potential partners across Audio, Film, Podcast & Gaming</p>
                    <button @click="loadAffiliatePartners()" class="bg-purple-600 hover:bg-purple-700 text-white px-6 py-2 rounded">
                        <i class="fas fa-users mr-2"></i>
                        Load Partners
                    </button>
                </div>
            </div>
        </div>
    </div>
</div>
`;

// Initialize Charts
function initializeCharts() {
    setTimeout(() => {
        // Market Trends Chart
        const ctx1 = document.getElementById('marketTrendsChart');
        if (ctx1) {
            new Chart(ctx1, {
                type: 'line',
                data: {
                    labels: ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 'Jul'],
                    datasets: [{
                        label: 'Market Size ($B)',
                        data: [1.8, 1.7, 1.9, 1.85, 2.1, 2.0, 2.4],
                        borderColor: '#3b82f6',
                        backgroundColor: 'rgba(59, 130, 246, 0.1)',
                        tension: 0.4,
                        fill: true,
                        pointRadius: 4,
                        pointHoverRadius: 6
                    }]
                },
                options: {
                    responsive: true,
                    maintainAspectRatio: false,
                    plugins: {
                        legend: { display: false }
                    },
                    scales: {
                        y: {
                            beginAtZero: false,
                            grid: { color: 'rgba(255, 255, 255, 0.1)' },
                            ticks: { color: '#9ca3af' }
                        },
                        x: {
                            grid: { color: 'rgba(255, 255, 255, 0.1)' },
                            ticks: { color: '#9ca3af' }
                        }
                    }
                }
            });
        }

        // Pain Points Chart
        const ctx2 = document.getElementById('painPointsChart');
        if (ctx2) {
            new Chart(ctx2, {
                type: 'doughnut',
                data: {
                    labels: ['Audio Pros', 'Photographers', 'Video Editors', 'Designers', 'Others'],
                    datasets: [{
                        data: [92, 87, 79, 73, 65],
                        backgroundColor: [
                            '#3b82f6',
                            '#8b5cf6',
                            '#ef4444',
                            '#f59e0b',
                            '#6b7280'
                        ]
                    }]
                },
                options: {
                    responsive: true,
                    maintainAspectRatio: false,
                    plugins: {
                        legend: {
                            position: 'bottom',
                            labels: {
                                color: '#9ca3af',
                                usePointStyle: true,
                                padding: 20
                            }
                        }
                    }
                }
            });
        }
    }, 100);
}

// Initialize
document.addEventListener('DOMContentLoaded', function() {
    document.querySelector('#app').innerHTML = dashboardHTML;
    window.intelligenceDashboard = intelligenceDashboard;
    
    // Initialize charts after DOM is ready
    initializeCharts();
});
