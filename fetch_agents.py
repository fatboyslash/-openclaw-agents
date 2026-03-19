import urllib.request
import re
import ssl

ssl_ctx = ssl.create_default_context()

base = "https://raw.githubusercontent.com/jnMetaCode/agency-agents-zh/main"

files_map = {
    "academic": [
        "academic-anthropologist.md",
        "academic-geographer.md",
        "academic-historian.md",
        "academic-narratologist.md",
        "academic-psychologist.md",
        "academic-study-planner.md",
    ],
    "design": [
        "design-brand-guardian.md",
        "design-image-prompt-engineer.md",
        "design-inclusive-visuals-specialist.md",
        "design-ui-designer.md",
        "design-ux-architect.md",
        "design-ux-researcher.md",
        "design-visual-storyteller.md",
        "design-whimsy-injector.md",
    ],
    "engineering": [
        "engineering-ai-data-remediation-engineer.md",
        "engineering-ai-engineer.md",
        "engineering-autonomous-optimization-architect.md",
        "engineering-backend-architect.md",
        "engineering-code-reviewer.md",
        "engineering-data-engineer.md",
        "engineering-database-optimizer.md",
        "engineering-devops-automator.md",
        "engineering-dingtalk-integration-developer.md",
        "engineering-embedded-firmware-engineer.md",
        "engineering-embedded-linux-driver-engineer.md",
        "engineering-feishu-integration-developer.md",
        "engineering-fpga-digital-design-engineer.md",
        "engineering-frontend-developer.md",
        "engineering-git-workflow-master.md",
        "engineering-incident-response-commander.md",
        "engineering-iot-solution-architect.md",
        "engineering-mobile-app-builder.md",
        "engineering-rapid-prototyper.md",
        "engineering-security-engineer.md",
        "engineering-senior-developer.md",
        "engineering-software-architect.md",
        "engineering-solidity-smart-contract-engineer.md",
        "engineering-sre.md",
        "engineering-technical-writer.md",
        "engineering-threat-detection-engineer.md",
        "engineering-wechat-mini-program-developer.md",
    ],
    "finance": [
        "finance-financial-forecaster.md",
        "finance-fraud-detector.md",
        "finance-invoice-manager.md",
    ],
    "hr": ["hr-performance-reviewer.md", "hr-recruiter.md"],
    "legal": ["legal-contract-reviewer.md", "legal-policy-writer.md"],
    "marketing": [
        "marketing-app-store-optimizer.md",
        "marketing-baidu-seo-specialist.md",
        "marketing-bilibili-strategist.md",
        "marketing-book-co-author.md",
        "marketing-carousel-growth-engine.md",
        "marketing-china-ecommerce-operator.md",
        "marketing-content-creator.md",
        "marketing-cross-border-ecommerce.md",
        "marketing-douyin-strategist.md",
        "marketing-ecommerce-operator.md",
        "marketing-growth-hacker.md",
        "marketing-instagram-curator.md",
        "marketing-knowledge-commerce-strategist.md",
        "marketing-kuaishou-strategist.md",
        "marketing-linkedin-content-creator.md",
        "marketing-livestream-commerce-coach.md",
        "marketing-podcast-strategist.md",
        "marketing-private-domain-operator.md",
        "marketing-reddit-community-builder.md",
        "marketing-seo-specialist.md",
        "marketing-short-video-editing-coach.md",
        "marketing-social-media-strategist.md",
        "marketing-tiktok-strategist.md",
        "marketing-twitter-engager.md",
        "marketing-wechat-official-account.md",
        "marketing-wechat-operator.md",
        "marketing-weibo-strategist.md",
        "marketing-weixin-channels-strategist.md",
        "marketing-xiaohongshu-operator.md",
        "marketing-xiaohongshu-specialist.md",
        "marketing-zhihu-strategist.md",
    ],
    "paid-media": [
        "paid-media-auditor.md",
        "paid-media-creative-strategist.md",
        "paid-media-paid-social-strategist.md",
        "paid-media-ppc-strategist.md",
        "paid-media-programmatic-buyer.md",
        "paid-media-search-query-analyst.md",
        "paid-media-tracking-specialist.md",
    ],
    "product": [
        "product-behavioral-nudge-engine.md",
        "product-feedback-synthesizer.md",
        "product-manager.md",
        "product-sprint-prioritizer.md",
        "product-trend-researcher.md",
    ],
    "project-management": [
        "project-management-experiment-tracker.md",
        "project-management-jira-workflow-steward.md",
        "project-management-project-shepherd.md",
        "project-management-studio-operations.md",
        "project-management-studio-producer.md",
        "project-manager-senior.md",
    ],
    "sales": [
        "sales-account-strategist.md",
        "sales-coach.md",
        "sales-deal-strategist.md",
        "sales-discovery-coach.md",
        "sales-engineer.md",
        "sales-outbound-strategist.md",
        "sales-pipeline-analyst.md",
        "sales-proposal-strategist.md",
    ],
    "spatial-computing": [
        "macos-spatial-metal-engineer.md",
        "terminal-integration-specialist.md",
        "visionos-spatial-engineer.md",
        "xr-cockpit-interaction-specialist.md",
        "xr-immersive-developer.md",
        "xr-interface-architect.md",
    ],
    "specialized": [
        "accounts-payable-agent.md",
        "agentic-identity-trust.md",
        "agents-orchestrator.md",
        "automation-governance-architect.md",
        "blockchain-security-auditor.md",
        "compliance-auditor.md",
        "corporate-training-designer.md",
        "data-consolidation-agent.md",
        "gaokao-college-advisor.md",
        "government-digital-presales-consultant.md",
        "healthcare-marketing-compliance.md",
        "identity-graph-operator.md",
        "lsp-index-engineer.md",
        "prompt-engineer.md",
        "report-distribution-agent.md",
        "sales-data-extraction-agent.md",
        "specialized-ai-policy-writer.md",
        "specialized-cultural-intelligence-strategist.md",
        "specialized-developer-advocate.md",
        "specialized-document-generator.md",
        "specialized-mcp-builder.md",
        "specialized-meeting-assistant.md",
        "specialized-model-qa.md",
        "specialized-pricing-optimizer.md",
        "specialized-risk-assessor.md",
        "specialized-salesforce-architect.md",
        "specialized-workflow-architect.md",
        "study-abroad-advisor.md",
        "zk-steward.md",
    ],
    "supply-chain": [
        "supply-chain-inventory-forecaster.md",
        "supply-chain-route-optimizer.md",
        "supply-chain-vendor-evaluator.md",
    ],
    "support": [
        "support-analytics-reporter.md",
        "support-executive-summary-generator.md",
        "support-finance-tracker.md",
        "support-infrastructure-maintainer.md",
        "support-legal-compliance-checker.md",
        "support-recruitment-specialist.md",
        "support-supply-chain-strategist.md",
        "support-support-responder.md",
    ],
    "testing": [
        "testing-accessibility-auditor.md",
        "testing-api-tester.md",
        "testing-embedded-qa-engineer.md",
        "testing-evidence-collector.md",
        "testing-performance-benchmarker.md",
        "testing-reality-checker.md",
        "testing-test-results-analyzer.md",
        "testing-tool-evaluator.md",
        "testing-workflow-optimizer.md",
    ],
    "game-development/unity": [
        "unity-architect.md",
        "unity-editor-tool-developer.md",
        "unity-multiplayer-engineer.md",
        "unity-shader-graph-artist.md",
    ],
    "game-development/unreal-engine": [
        "unreal-multiplayer-architect.md",
        "unreal-systems-engineer.md",
        "unreal-technical-artist.md",
        "unreal-world-builder.md",
    ],
    "game-development/godot": [
        "godot-gameplay-scripter.md",
        "godot-multiplayer-engineer.md",
        "godot-shader-developer.md",
    ],
    "game-development/blender": ["blender-addon-engineer.md"],
    "game-development/roblox-studio": [
        "roblox-avatar-creator.md",
        "roblox-experience-designer.md",
        "roblox-systems-scripter.md",
    ],
}

results = []

for category, filenames in files_map.items():
    for fname in filenames:
        url = f"{base}/{category}/{fname}"
        try:
            req = urllib.request.Request(url, headers={"User-Agent": "Mozilla/5.0"})
            resp = urllib.request.urlopen(req, context=ssl_ctx, timeout=15)
            content = resp.read().decode("utf-8")
            m = re.match(r"^---\s*\n(.*?)\n---", content, re.DOTALL)
            if m:
                fm = m.group(1)
                name_m = re.search(r"^name:\s*(.+)$", fm, re.MULTILINE)
                desc_m = re.search(r"^description:\s*(.+)$", fm, re.MULTILINE)
                color_m = re.search(r"^color:\s*(.+)$", fm, re.MULTILINE)
                name = name_m.group(1).strip() if name_m else "N/A"
                desc = desc_m.group(1).strip() if desc_m else "N/A"
                color = color_m.group(1).strip() if color_m else "N/A"
            else:
                name = desc = color = "PARSE_ERROR"
            results.append((category, fname, name, desc, color))
        except Exception as e:
            results.append((category, fname, "ERROR", str(e), ""))

import io

out = io.open("agents_result.txt", "w", encoding="utf-8")
for r in results:
    out.write(f"{r[0]} | {r[1]} | {r[2]} | {r[3]} | {r[4]}\n")
out.write(f"\nTotal: {len(results)}\n")
out.close()
print(f"Done. Total: {len(results)}")
