# Optional local LaMini-Flan-T5 provider

The supplied documentation mentions LaMini-Flan-T5-783M for concept explanation.

The standard EduGenie installation deliberately does not install PyTorch/Transformers because those packages make the setup much larger and hardware-dependent. The application therefore uses Gemini for explanations by default.

If you later want a local provider, install compatible versions of `torch` and `transformers` for your operating system, then implement `_local_explanation()` in `explanation_module.py` and set:

```text
EXPLANATION_PROVIDER=local
```

The public `/explain` endpoint does not need to change.
