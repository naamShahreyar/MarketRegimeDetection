from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import cm
from reportlab.lib import colors
from reportlab.platypus import (
    SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle,
    HRFlowable, PageBreak
)
from reportlab.lib.enums import TA_LEFT, TA_CENTER, TA_JUSTIFY
from reportlab.platypus import KeepTogether
import os

OUTPUT_PATH = os.path.join(os.path.dirname(__file__), "MarketRegimeDetection.pdf")

PAGE_W, PAGE_H = A4
MARGIN = 2.2 * cm

doc = SimpleDocTemplate(
    OUTPUT_PATH,
    pagesize=A4,
    leftMargin=MARGIN,
    rightMargin=MARGIN,
    topMargin=2.5 * cm,
    bottomMargin=2.2 * cm,
    title="Market Regime Detection and Dynamic Portfolio Allocation",
    author="naamShahreyar",
)

BASE = getSampleStyleSheet()

# Custom styles
def style(name, parent="Normal", **kw):
    s = ParagraphStyle(name, parent=BASE[parent], **kw)
    return s

H1 = style("H1", "Heading1", fontSize=22, leading=28, spaceAfter=6,
           textColor=colors.HexColor("#0d1b2a"), fontName="Helvetica-Bold")

H2 = style("H2", "Heading2", fontSize=14, leading=18, spaceBefore=18,
           spaceAfter=6, textColor=colors.HexColor("#1b4f72"), fontName="Helvetica-Bold")

H3 = style("H3", "Heading3", fontSize=11, leading=15, spaceBefore=10,
           spaceAfter=4, textColor=colors.HexColor("#1a5276"), fontName="Helvetica-Bold")

BODY = style("Body", fontSize=10, leading=15, spaceAfter=6,
             textColor=colors.HexColor("#222222"), alignment=TA_JUSTIFY)

CODE = style("Code", fontSize=8.5, leading=13, fontName="Courier",
             backColor=colors.HexColor("#f4f6f8"),
             leftIndent=12, rightIndent=12, spaceBefore=4, spaceAfter=4,
             textColor=colors.HexColor("#1a252f"))

CAPTION = style("Caption", fontSize=8.5, leading=12, spaceAfter=4,
                textColor=colors.HexColor("#555555"), alignment=TA_CENTER,
                fontName="Helvetica-Oblique")

SUBTITLE = style("Subtitle", fontSize=12, leading=16, spaceAfter=20,
                 textColor=colors.HexColor("#555555"), alignment=TA_CENTER,
                 fontName="Helvetica-Oblique")

COVER_TITLE = style("CoverTitle", fontSize=28, leading=34, spaceAfter=12,
                    textColor=colors.HexColor("#0d1b2a"), fontName="Helvetica-Bold",
                    alignment=TA_CENTER)


def hr(color="#1b4f72", width=0.8):
    return HRFlowable(width="100%", thickness=width,
                      color=colors.HexColor(color), spaceAfter=8, spaceBefore=4)


def table(data, col_widths, header_bg="#1b4f72"):
    t = Table(data, colWidths=col_widths)
    n_rows = len(data)
    style_cmds = [
        ("BACKGROUND", (0, 0), (-1, 0), colors.HexColor(header_bg)),
        ("TEXTCOLOR", (0, 0), (-1, 0), colors.white),
        ("FONTNAME", (0, 0), (-1, 0), "Helvetica-Bold"),
        ("FONTSIZE", (0, 0), (-1, 0), 9),
        ("FONTNAME", (0, 1), (-1, -1), "Helvetica"),
        ("FONTSIZE", (0, 1), (-1, -1), 9),
        ("ROWBACKGROUNDS", (0, 1), (-1, -1),
         [colors.HexColor("#eaf0fb"), colors.white]),
        ("GRID", (0, 0), (-1, -1), 0.4, colors.HexColor("#b0bec5")),
        ("ALIGN", (0, 0), (-1, -1), "LEFT"),
        ("VALIGN", (0, 0), (-1, -1), "MIDDLE"),
        ("TOPPADDING", (0, 0), (-1, -1), 5),
        ("BOTTOMPADDING", (0, 0), (-1, -1), 5),
        ("LEFTPADDING", (0, 0), (-1, -1), 8),
        ("RIGHTPADDING", (0, 0), (-1, -1), 8),
    ]
    t.setStyle(TableStyle(style_cmds))
    return t


story = []

# ── Cover page ──────────────────────────────────────────────────────────────
story.append(Spacer(1, 3.5 * cm))
story.append(Paragraph("Market Regime Detection", COVER_TITLE))
story.append(Paragraph("and Dynamic Portfolio Allocation", COVER_TITLE))
story.append(Spacer(1, 0.6 * cm))
story.append(hr(width=2))
story.append(Spacer(1, 0.4 * cm))
story.append(Paragraph(
    "A regime-based systematic trading strategy using a Hidden Markov Model "
    "to identify latent market states and dynamically size positions in SPY "
    "based on the estimated probability of a risk-on regime.",
    SUBTITLE
))
story.append(Spacer(1, 1.5 * cm))

meta = [
    ["Author", "naamShahreyar"],
    ["Data Range", "January 2005 - Present"],
    ["Model", "Gaussian HMM  (K = 2, full covariance)"],
    ["Universe", "SPY, TLT, GLD, VIX"],
    ["Benchmark", "SPY Buy-and-Hold"],
]
story.append(table(meta, [4.5 * cm, 11 * cm], header_bg="#0d1b2a"))
story.append(PageBreak())

# ── 1. Overview ──────────────────────────────────────────────────────────────
story.append(Paragraph("1. Overview", H1))
story.append(hr())
story.append(Paragraph(
    "Financial markets do not evolve as a single stationary process. "
    "They periodically shift between distinct regimes: calm, trending "
    "periods characterised by low volatility and positive momentum, and "
    "stress periods marked by elevated volatility, large drawdowns, and "
    "flight-to-safety flows. Identifying the current regime in real time "
    "enables a portfolio manager to modulate risk exposure rather than "
    "maintaining a fixed allocation throughout the cycle.", BODY
))
story.append(Paragraph(
    "This project models those regimes in an unsupervised fashion using a "
    "Gaussian Hidden Markov Model (HMM) trained on a multi-asset feature set. "
    "Rather than assigning hard regime labels, the model outputs a continuous "
    "probability of being in a risk-on state. That probability is used to "
    "scale SPY exposure dynamically, with leverage capped at 2x and "
    "5 basis-point-per-unit transaction costs applied to every rebalance.", BODY
))
story.append(Spacer(1, 0.3 * cm))

# ── 2. Project Structure ──────────────────────────────────────────────────────
story.append(Paragraph("2. Project Structure", H1))
story.append(hr())

struct = (
    "MarketRegimeDetection/<br/>"
    "&nbsp;&nbsp;&nbsp;&nbsp;data/<br/>"
    "&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;raw/market_prices.csv<br/>"
    "&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;processed/features.csv<br/>"
    "&nbsp;&nbsp;&nbsp;&nbsp;notebooks/<br/>"
    "&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;01_data_collection.ipynb<br/>"
    "&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;02_feature_engineering.ipynb<br/>"
    "&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;03_hmm_modelling.ipynb<br/>"
    "&nbsp;&nbsp;&nbsp;&nbsp;requirements.txt<br/>"
    "&nbsp;&nbsp;&nbsp;&nbsp;README.md"
)
story.append(Paragraph(struct, CODE))
story.append(Spacer(1, 0.2 * cm))
story.append(Paragraph(
    "The pipeline is split across three sequential notebooks. Each notebook "
    "writes its output to disk so the next step can be run independently.", BODY
))
story.append(Spacer(1, 0.3 * cm))

# ── 3. Data ──────────────────────────────────────────────────────────────────
story.append(Paragraph("3. Data", H1))
story.append(hr())
story.append(Paragraph(
    "Daily adjusted close prices are downloaded via the <b>yfinance</b> library "
    "starting 2005-01-01. Four instruments are collected to capture both equity "
    "risk and cross-asset regime signals:", BODY
))
story.append(Spacer(1, 0.15 * cm))

data_tbl = [
    ["Ticker", "Asset", "Role in feature set"],
    ["SPY", "SPDR S&P 500 ETF", "Primary trading vehicle and core feature source"],
    ["TLT", "iShares 20+ Year Treasury ETF", "Flight-to-safety / risk-off signal"],
    ["GLD", "SPDR Gold ETF", "Safe-haven / inflation signal"],
    ["^VIX", "CBOE Volatility Index", "Equity fear gauge; used as a level feature"],
]
story.append(table(data_tbl, [2.2 * cm, 5.5 * cm, 7.8 * cm]))
story.append(Spacer(1, 0.2 * cm))
story.append(Paragraph(
    "A single missing observation per equity ticker (one non-trading day) is "
    "filled forward. The raw prices are saved to <i>data/raw/market_prices.csv</i>.", BODY
))
story.append(Spacer(1, 0.3 * cm))

# ── 4. Feature Engineering ────────────────────────────────────────────────────
story.append(Paragraph("4. Feature Engineering", H1))
story.append(hr())
story.append(Paragraph(
    "Nine features are constructed to capture the multi-dimensional nature of "
    "market regimes. Features span volatility, trend, drawdown, cross-asset "
    "momentum, and the fear gauge:", BODY
))
story.append(Spacer(1, 0.15 * cm))

feat_tbl = [
    ["Feature", "Description"],
    ["SPY_vol_20", "20-day annualized rolling standard deviation of SPY daily returns"],
    ["SPY_price_ma50", "SPY price divided by its 50-day simple moving average"],
    ["SPY_price_ma200", "SPY price divided by its 200-day simple moving average"],
    ["SPY_drawdown", "Drawdown of SPY from its rolling all-time high"],
    ["VIX_level", "Raw daily close of the VIX index"],
    ["TLT_ret_20", "20-day return of TLT (captures bond market flight-to-safety)"],
    ["GLD_ret_20", "20-day return of GLD (captures safe-haven demand)"],
    ["SPY_ret_5", "5-day return of SPY (short-term momentum)"],
    ["SPY_ret_20", "20-day return of SPY (medium-term momentum)"],
]
story.append(table(feat_tbl, [4 * cm, 11.5 * cm]))
story.append(Spacer(1, 0.2 * cm))
story.append(Paragraph(
    "The 200-day moving average window means the feature matrix begins "
    "2005-10-17. All NaN rows are dropped before modelling. The resulting "
    "dataset spans roughly 5,100 trading days. Features are standardised using "
    "StandardScaler fitted on the training split and applied to both splits.", BODY
))
story.append(Spacer(1, 0.3 * cm))

# ── 5. Methodology ────────────────────────────────────────────────────────────
story.append(Paragraph("5. Methodology", H1))
story.append(hr())

story.append(Paragraph("5.1  Train / Test Split", H2))
story.append(Paragraph(
    "The feature matrix is sorted chronologically and split 70 / 30. "
    "No shuffling is applied; the split respects temporal order to prevent "
    "look-ahead bias. The StandardScaler is fit exclusively on the training "
    "set and then applied to both sets.", BODY
))

story.append(Paragraph("5.2  Choosing the Number of Regimes", H2))
story.append(Paragraph(
    "Three complementary diagnostics were used to select K:", BODY
))
story.append(Paragraph(
    "<b>Elbow method</b> on KMeans inertia: the elbow in the inertia curve "
    "suggested K = 4 as a plausible candidate.", BODY
))
story.append(Paragraph(
    "<b>Silhouette score</b>: averaged over all samples, K = 2 produced the "
    "highest silhouette score, indicating well-separated, compact clusters.", BODY
))
story.append(Paragraph(
    "<b>PCA cluster visualisation</b>: projecting the training set onto its "
    "first two principal components showed K = 3 and K = 4 to produce "
    "heavily overlapping clusters. K = 2 gave the clearest separation.", BODY
))
story.append(Paragraph("K = 2 was selected.", BODY))

story.append(Paragraph("5.3  Gaussian HMM", H2))
story.append(Paragraph(
    "A Gaussian HMM with full covariance matrices is trained on the "
    "standardised training data. Full covariance allows the model to capture "
    "correlations between features within each regime state.", BODY
))
story.append(Spacer(1, 0.1 * cm))
story.append(Paragraph(
    "GaussianHMM(n_components=2, covariance_type='full', n_iter=1000, random_state=42).fit(X_train)",
    CODE
))
story.append(Spacer(1, 0.1 * cm))
story.append(Paragraph(
    "After fitting, <b>predict_proba</b> is called on the full (scaled) dataset "
    "to obtain a daily time series of regime probabilities. These soft "
    "probabilities drive position sizing rather than discrete regime labels.", BODY
))
story.append(Spacer(1, 0.3 * cm))

# ── 6. Regime Interpretation ──────────────────────────────────────────────────
story.append(Paragraph("6. Regime Interpretation", H1))
story.append(hr())
story.append(Paragraph(
    "The two regimes were characterised by computing mean feature values "
    "grouped by regime label on the training set:", BODY
))
story.append(Spacer(1, 0.15 * cm))

regime_tbl = [
    ["Regime", "SPY 20d Return", "SPY Volatility", "VIX Level", "SPY Drawdown", "Interpretation"],
    ["0", "-0.25%", "22.6%", "25.6", "-17.7%", "Crisis / Risk-off"],
    ["1", "+1.40%", "10.3%", "14.0", "-1.2%", "Bull / Risk-on"],
]
story.append(table(regime_tbl, [1.5 * cm, 2.8 * cm, 3 * cm, 2.4 * cm, 3 * cm, 3.3 * cm]))
story.append(Spacer(1, 0.2 * cm))
story.append(Paragraph(
    "Regime 0 corresponds to market stress: negative returns, volatility above "
    "20%, VIX near 25, and deep drawdowns. Regime 1 captures the normal bull "
    "market environment with a VIX near 14 and minimal drawdown.", BODY
))
story.append(Spacer(1, 0.3 * cm))

# ── 7. Historical Validation ──────────────────────────────────────────────────
story.append(Paragraph("7. Historical Regime Validation", H1))
story.append(hr())
story.append(Paragraph(
    "To validate that the model correctly identifies known crisis periods, the "
    "share of days classified as Regime 0 (crisis) was computed for three "
    "distinct historical episodes:", BODY
))
story.append(Spacer(1, 0.15 * cm))

val_tbl = [
    ["Episode", "Window", "Regime 0 (Crisis) Share"],
    ["2008 Global Financial Crisis", "Jan 2008 - Jun 2009", "100%"],
    ["COVID-19 Crash", "Feb 2020 - Jun 2020", "83%"],
    ["2022 Inflation Shock", "Jan 2022 - Oct 2022", "94%"],
]
story.append(table(val_tbl, [5.5 * cm, 5 * cm, 5 * cm]))
story.append(Spacer(1, 0.2 * cm))
story.append(Paragraph(
    "All three episodes were overwhelmingly classified as Regime 0, "
    "confirming that the HMM learns economically meaningful states rather "
    "than arbitrary statistical clusters.", BODY
))
story.append(Spacer(1, 0.3 * cm))

# ── 8. Strategy Logic ─────────────────────────────────────────────────────────
story.append(Paragraph("8. Strategy Logic", H1))
story.append(hr())
story.append(Paragraph(
    "Position size is a continuous, monotone function of the risk-on "
    "probability. This avoids the whipsawing that comes from hard "
    "regime switches and scales exposure proportionally to conviction:", BODY
))
story.append(Spacer(1, 0.1 * cm))
story.append(Paragraph("position = clip(p_risk_on * 2, 0, 2)", CODE))
story.append(Spacer(1, 0.1 * cm))
story.append(Paragraph(
    "At p_risk_on = 1.0 the strategy holds 2x leveraged SPY. "
    "At p_risk_on = 0.5 it holds 1x. At p_risk_on = 0.0 it is flat. "
    "The position is executed on the next day's open (shifted by one period).", BODY
))

story.append(Paragraph("Transaction Costs", H3))
story.append(Paragraph(
    "A per-unit transaction cost of 5 basis points is charged on every "
    "change in position size:", BODY
))
story.append(Paragraph(
    "turnover = |position - position.shift(1)|<br/>"
    "transaction_cost = 0.0005 * turnover<br/>"
    "strategy_return = position.shift(1) * SPY_ret - transaction_cost",
    CODE
))
story.append(Spacer(1, 0.3 * cm))

# ── 9. Backtest Results ───────────────────────────────────────────────────────
story.append(Paragraph("9. Backtest Results", H1))
story.append(hr())
story.append(Paragraph(
    "Performance is evaluated over the full dataset from late 2005 to the "
    "present, covering the 2008 financial crisis, the 2020 pandemic crash, "
    "the 2022 rate-hike cycle, and the 2025-26 tariff shock:", BODY
))
story.append(Spacer(1, 0.2 * cm))

perf_tbl = [
    ["Metric", "Buy and Hold (SPY)", "Regime Strategy"],
    ["Sharpe Ratio", "0.65", "0.79"],
    ["Sortino Ratio", "0.61", "0.80"],
    ["Maximum Drawdown", "-55%", "-30%"],
    ["Total Return", "8.04x", "9.99x"],
]
story.append(table(perf_tbl, [5.5 * cm, 4.5 * cm, 4.5 * cm]))
story.append(Spacer(1, 0.2 * cm))
story.append(Paragraph(
    "The regime strategy improves the Sharpe ratio from 0.65 to 0.79 "
    "and the Sortino ratio from 0.61 to 0.80, while cutting maximum drawdown "
    "nearly in half (from -55% to -30%). Total return over the full period "
    "increases from 8.04x to 9.99x despite the drag from transaction costs "
    "and periods of reduced or zero exposure.", BODY
))
story.append(Spacer(1, 0.2 * cm))
story.append(Paragraph(
    "The reduction in maximum drawdown is the most practically significant "
    "result. A 30% peak-to-trough loss is materially easier to sustain and "
    "recover from than a 55% loss, both psychologically and in terms of the "
    "return required to get back to the prior high (43% vs 122%).", BODY
))
story.append(Spacer(1, 0.3 * cm))

# ── 10. Installation ──────────────────────────────────────────────────────────
story.append(Paragraph("10. Installation and Usage", H1))
story.append(hr())
story.append(Paragraph("Clone the repository and install dependencies:", BODY))
story.append(Paragraph(
    "git clone https://github.com/naamShahreyar/MarketRegimeDetection.git<br/>"
    "cd MarketRegimeDetection<br/>"
    "pip install -r requirements.txt",
    CODE
))
story.append(Spacer(1, 0.15 * cm))
story.append(Paragraph("Run the notebooks in order:", BODY))
story.append(Paragraph(
    "1. notebooks/01_data_collection.ipynb<br/>"
    "2. notebooks/02_feature_engineering.ipynb<br/>"
    "3. notebooks/03_hmm_modelling.ipynb",
    CODE
))
story.append(Spacer(1, 0.15 * cm))
story.append(Paragraph(
    "Each notebook writes its output to the <i>data/</i> directory so that "
    "subsequent notebooks can be run independently without re-executing "
    "earlier steps.", BODY
))
story.append(Spacer(1, 0.3 * cm))

# ── 11. Dependencies ──────────────────────────────────────────────────────────
story.append(Paragraph("11. Dependencies", H1))
story.append(hr())

deps_tbl = [
    ["Package", "Purpose"],
    ["pandas", "Data manipulation and time-series alignment"],
    ["numpy", "Numerical operations and array math"],
    ["yfinance", "Downloading historical market data from Yahoo Finance"],
    ["matplotlib", "Visualisation of price series, regimes, and backtest curves"],
    ["seaborn", "Statistical plots (boxplots, heatmaps)"],
    ["scikit-learn", "StandardScaler, KMeans, PCA, silhouette_score"],
    ["hmmlearn", "Gaussian HMM implementation"],
]
story.append(table(deps_tbl, [3.5 * cm, 12 * cm]))

doc.build(story)
print(f"PDF written to: {OUTPUT_PATH}")
