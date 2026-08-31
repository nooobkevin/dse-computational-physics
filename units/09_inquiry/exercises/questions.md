# Scientific Inquiry — Concept Questions

These questions test your understanding of the scientific inquiry process
and data analysis techniques used in the exercise.  Answer them in a few
sentences each.

---

## Questions

### (a) Identifying variables

You are designing an experiment to investigate how the period of a simple
pendulum depends on its length.

1. What is the **independent variable**?
2. What is the **dependent variable**?
3. List at least **three control variables** that must be kept constant.

**（a）辨識變量**

你正設計一個實驗，探究單擺的週期如何隨其長度而變化。

1. 甚麼是**自變量**？
2. 甚麼是**因變量**？
3. 列出至少**三項**必須保持恆定的控制變量。

### (b) Why linearise?

You collect (L, T) data from a pendulum experiment.  The relationship
between T and L is non-linear: T = 2π √(L/g).

1. Why do we plot T² vs L instead of T vs L?
2. What quantity does the slope of the T² vs L graph represent?
3. What would the intercept be if the data were perfect?

**（b）為甚麼要線性化？**

你從單擺實驗收集了 (L, T) 數據。T 與 L 的關係是非線性的：T = 2π √(L/g)。

1. 為甚麼我們繪 T² 對 L 的圖，而不是 T 對 L 的圖？
2. T² 對 L 圖的斜率代表甚麼物理量？
3. 若數據完美，截距會是多少？

### (c) Best-fit line vs passing through origin

When you fit a straight line to the T² vs L data, the best-fit line may
not pass exactly through the origin (0, 0), even though theory predicts
it should.

1. Why might the best-fit line not pass through the origin?
2. Should you force the line through the origin?  Explain the trade-off.
3. What does a non-zero intercept tell you about your data or experiment?

**（c）最佳擬合線與通過原點**

當你對 T² 對 L 數據擬合一條直線時，最佳擬合線可能不會恰好通過原點 (0, 0)，即使理論預測它應該通過。

1. 為甚麼最佳擬合線可能不通過原點？
2. 你應否強迫直線通過原點？解釋當中的取捨。
3. 非零截距告訴你關於數據或實驗的甚麼？

### (d) Percent error

You estimate g = 9.65 m/s² from your pendulum data.  The accepted value
is g = 9.81 m/s².

1. Compute the percent error of your estimate.
2. Is this a small or large error?  What might cause it?
3. How would the percent error change if you used a longer pendulum?

**（d）百分誤差**

你從單擺數據估算出 g = 9.65 m/s²。公認值為 g = 9.81 m/s²。

1. 計算你估算值的百分誤差。
2. 這是小誤差還是大誤差？可能是甚麼造成的？
3. 若你使用較長的單擺，百分誤差會如何變化？

### (e) Systematic vs random error

Classify each of the following as **systematic** or **random** error:

1. Air resistance slowing the pendulum swing.
2. Parallax error when reading the angle from a protractor.
3. Human reaction time when starting/stopping a stopwatch.
4. The small-angle approximation (sin θ ≈ θ).
5. Pixel-tracking jitter in video analysis.

For each, explain whether it makes the measured period longer, shorter, or
unpredictable.

**（e）系統誤差與隨機誤差**

將以下各項分類為**系統誤差**或**隨機誤差**：

1. 空氣阻力使單擺擺動減慢。
2. 用量角器讀取角度時的視差誤差。
3. 啟動／停止秒錶時的人類反應時間。
4. 小角度近似（sin θ ≈ θ）。
5. 影片分析中的像素追蹤抖動。

對每一項，解釋它使量得的週期變長、變短，還是不可預測。

### (f) Evaluation and limitations

After completing your experiment and analysis, you are asked to evaluate
your investigation.

1. List at least **two limitations** of your experimental design.
2. Suggest **one improvement** to reduce the dominant source of error.
3. How confident are you in your estimated value of g?  What evidence
   supports your confidence?
4. If your percent error is large, does that mean the experiment was a
   failure?  Explain.

**（f）評估與限制**

完成實驗與分析後，你被要求評估你的探究。

1. 列出你實驗設計的至少**兩項限制**。
2. 建議**一項**改善，以減少最主要的誤差來源。
3. 你對估算的 g 值有多大信心？甚麼證據支持你的信心？
4. 若你的百分誤差很大，是否表示實驗失敗？解釋。

---

## Model Answers (teacher only) 模型答案（僅供教師）

*The section below contains model answers.  Remove it before distributing
the questions to students.*

---

### (a) Model answer

1. **Independent variable**: Length of the pendulum (L).
2. **Dependent variable**: Period of oscillation (T).
3. **Control variables**: Mass of the bob, initial angular displacement
   (amplitude), air resistance (same environment), release method (no
   initial push), timing method.

### (b) Model answer

1. Plotting T² vs L linearises the relationship: T² = (4π²/g) × L is a
   straight line through the origin.  A straight line is easier to fit,
   analyse, and interpret than a curve.
2. The slope represents 4π²/g.  From the slope, we can estimate g:
   g = 4π² / slope.
3. The intercept should be zero (T² = 0 when L = 0).

### (c) Model answer

1. A non-zero intercept can arise from measurement errors (systematic
   offset in timing, incorrect length measurement), or from the fact that
   the pendulum has a finite bob size (effective length ≠ measured length).
2. Forcing through the origin is generally not recommended unless you are
   certain the relationship passes through (0, 0).  Forcing can bias the
   slope estimate.  It is better to fit freely and examine the intercept
   — if it is close to zero, the model is validated.
3. A non-zero intercept suggests either a systematic error in the
   measurements or that the assumed model (T² = (4π²/g) × L) is incomplete
   (e.g., the effective length includes the bob radius).

### (d) Model answer

1. Percent error = |9.65 - 9.81| / 9.81 × 100 ≈ 1.63%.
2. This is a relatively small error (~1.6%), suggesting the experiment was
   reasonably accurate.  Possible causes: air resistance, small-angle
   approximation error, timing precision, length measurement error.
3. A longer pendulum has a longer period, which reduces the relative
   effect of timing errors (fixed ±0.1 s reaction time is a smaller
   fraction of a longer period).  So percent error would likely decrease.

### (e) Model answer

| Source | Type | Effect on period |
|--------|------|-----------------|
| Air resistance | Systematic | Increases T (slows the pendulum) |
| Parallax error | Random | Unpredictable (random scatter) |
| Human reaction time | Random | Random scatter (±0.1–0.2 s) |
| Small-angle approximation | Systematic | True period is slightly longer than predicted |
| Pixel-tracking jitter | Random | Random noise in angle measurement |

### (f) Model answer

1. **Limitations**: (i) Small-angle approximation introduces systematic
   error; (ii) human reaction time limits timing precision; (iii) only
   one trial per length (no repeat measurements to estimate uncertainty).
2. **Improvement**: Use a photogate or light sensor with a data logger to
   measure the period automatically, eliminating human reaction time.
   Repeat measurements at each length to estimate random uncertainty.
3. Confidence is supported by: R² close to 1 (good linear fit), small
   percent error, and consistency with the theoretical model.  If R² is
   low or percent error is large, confidence is reduced.
4. No — a large percent error is not a failure.  It is an opportunity to
   identify sources of error, improve the experimental design, and learn
about the limitations of the measurement.  Science progresses by
    understanding and reducing errors.

---

### (g) Critically evaluating AI-generated analysis

You use an AI tool to analyse your pendulum data.  The AI outputs:

```
Fit: T² = 4.12 × L + 0.08
g = 4π² / 4.12 = 9.58 m/s²
Percent error vs 9.81 = 2.34%
Conclusion: the data strongly supports the theoretical model.
```

1. The AI claims the data "strongly supports the model."  What additional
   information would you need to verify this claim?  (Hint: what does the
   AI not show you?)

2. The intercept is +0.08 s², but theory predicts 0.  Should this change
   your confidence in the AI's conclusion?  Explain.

3. If you fed the AI raw (L, T) data and it produced the T² vs L plot
   and fit automatically, what potential pitfalls might you miss?

4. How would you critically evaluate the reliability and scientific accuracy
   of this AI-generated output?  List at least two steps you would take.

**（g）批判性評估 AI 生成的分析**

你使用 AI 工具分析你的單擺數據。AI 輸出：

```
Fit: T² = 4.12 × L + 0.08
g = 4π² / 4.12 = 9.58 m/s²
Percent error vs 9.81 = 2.34%
Conclusion: the data strongly supports the theoretical model.
```

1. AI 聲稱數據「強烈支持該模型」。你需要甚麼額外資訊來核實這個說法？（提示：AI 沒有向你展示甚麼？）
2. 截距為 +0.08 s²，但理論預測為 0。這應否改變你對 AI 結論的信心？解釋。
3. 若你把原始 (L, T) 數據交給 AI，它自動產生 T² 對 L 圖並擬合，你可能會忽略哪些潛在陷阱？
4. 你會如何批判性評估這份 AI 生成輸出的可靠性與科學準確性？列出你至少會採取的兩項步驟。

### (h) Safety assessment

You are designing an experiment to measure the acceleration due to gravity
by dropping a steel ball from a height of 2.0 m and timing its fall with
a stopwatch.  The experiment will be performed in a school laboratory.

1. Identify **two** potential safety hazards in this experiment.

2. For each hazard, suggest a control measure to reduce the risk.

3. You decide to use a heavier (5 kg) ball instead of a small steel ball
   to get a more "reliable" measurement.  Is this a safety concern?
   Explain.

4. Your friend suggests using the school rooftop (height ≈ 10 m) to get
   a longer fall time and reduce the relative timing error.  What safety
   concerns does this raise?  How would you address them while still
   improving measurement accuracy?

**（h）安全評估**

你正設計一個實驗，從 2.0 m 高度釋放鋼球並用秒錶計時其下落，以量度重力加速度。實驗將在校內實驗室進行。

1. 辨識此實驗中**兩項**潛在安全危害。
2. 對每項危害，建議一項控制措施以降低風險。
3. 你決定改用較重（5 kg）的球而非小鋼球，以獲得更「可靠」的量度。這是安全問題嗎？解釋。
4. 你的朋友建議使用學校天台（高度約 10 m）以獲得更長的下落時間並減少相對計時誤差。這會引起甚麼安全問題？你會如何在仍改善量度準確度的同時處理這些問題？

---

## Model Answers (teacher only) 模型答案（僅供教師）

*The section below contains model answers.  Remove it before distributing
the questions to students.*

---
