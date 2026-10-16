"""Create the self-contained Day 1 Colab notebook without notebook dependencies."""

import json
from pathlib import Path
from textwrap import dedent


ROOT = Path(__file__).resolve().parents[1]
OUTPUT = ROOT / "notebooks" / "01_tokenizer_embeddings.ipynb"


def markdown(source):
    return {"cell_type": "markdown", "metadata": {}, "source": dedent(source).strip().splitlines(True)}


def code(source):
    return {
        "cell_type": "code",
        "execution_count": None,
        "metadata": {},
        "outputs": [],
        "source": dedent(source).strip().splitlines(True),
    }


cells = [
    markdown("""
    # Day 1 · Tokens in, logits out

    **Objective:** Build a byte tokenizer and a small byte-level BPE tokenizer from scratch. Trace token IDs through an embedding table and LM head to next-token logits, then compare vocabulary size, sequence length, and parameter count.

    **Environment:** Google Colab CPU; Python 3.10+, PyTorch, Matplotlib. No GPU or external dataset required.  
    **Seed:** 42. **Expected runtime:** under 3 minutes on a typical Colab CPU.  
    **Scope:** The `TokenToLogits` module below has no attention or recurrent layer. It only sees the token at the current position, so it is an I/O demonstration and a bigram-like baseline, not a contextual Transformer.

    [![Open in Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/yanxulab/yanxulab.github.io/blob/main/notebooks/01_tokenizer_embeddings.ipynb)
    """),
    markdown("""
    ## 1. A tiny, fixed corpus

    Keep the training corpus separate from the held-out text. All tokenizer vocabulary sizes below are learned from exactly the same training strings.
    """),
    code("""
    from collections import Counter
    from random import seed as random_seed

    SEED = 42
    random_seed(SEED)

    train_texts = [
        "the model reads tokens and predicts the next token.",
        "tokens become vectors through an embedding table.",
        "a language model maps hidden vectors to vocabulary logits.",
        "the tokenizer turns text into token ids and back into text.",
        "a small vocabulary creates longer sequences of tokens.",
        "a larger vocabulary stores more entries in the embedding table.",
        "the model reads the text one token at a time.",
        "the next token depends on the previous context in a real model.",
    ]
    held_out = "the Transformer reads unseen words and emoji 🚀."
    print("Training UTF-8 bytes:", sum(len(t.encode("utf-8")) for t in train_texts))
    print("Held-out text:", held_out)
    """),
    markdown("""
    ## 2. The byte baseline

    UTF-8 turns text into bytes numbered 0–255. Every valid Unicode string can be reconstructed, so a byte tokenizer has no unknown-token (`<UNK>`) problem; the cost is that one visible character can occupy several byte tokens.
    """),
    code("""
    def byte_encode(text):
        return list(text.encode("utf-8"))

    def byte_decode(ids):
        return bytes(ids).decode("utf-8")

    byte_ids = byte_encode(held_out)
    assert byte_decode(byte_ids) == held_out
    print("Byte vocab size: 256")
    print("Token count:", len(byte_ids))
    print("First 24 token IDs:", byte_ids[:24])
    print("Rocket UTF-8 bytes:", byte_encode("🚀"))
    """),
    markdown("""
    ## 3. Train byte-level BPE from scratch

    Start with the 256 byte tokens. Repeatedly find the most frequent adjacent token pair **within each training string**, assign the pair a new token ID, and merge its non-overlapping occurrences. At encoding time, replay the learned merges in training order. This is a deliberately small teaching implementation: production byte-level BPE tokenizers also make choices about pre-tokenization and special tokens.
    """),
    code("""
    def merge_pair(ids, pair, new_id):
        merged = []
        i = 0
        while i < len(ids):
            if i + 1 < len(ids) and (ids[i], ids[i + 1]) == pair:
                merged.append(new_id)
                i += 2
            else:
                merged.append(ids[i])
                i += 1
        return merged


    def train_byte_bpe(texts, max_merges):
        sequences = [byte_encode(text) for text in texts]
        token_bytes = [bytes([i]) for i in range(256)]
        merges = []
        for _ in range(max_merges):
            counts = Counter(
                (left, right)
                for ids in sequences
                for left, right in zip(ids, ids[1:])
            )
            if not counts:
                break
            # Deterministic tie-breaking keeps the notebook reproducible.
            pair = min(counts, key=lambda p: (-counts[p], p))
            new_id = len(token_bytes)
            token_bytes.append(token_bytes[pair[0]] + token_bytes[pair[1]])
            merges.append(pair)
            sequences = [merge_pair(ids, pair, new_id) for ids in sequences]
        return merges, token_bytes


    def bpe_encode(text, merges):
        ids = byte_encode(text)
        for new_id, pair in enumerate(merges, start=256):
            ids = merge_pair(ids, pair, new_id)
        return ids


    def bpe_decode(ids, token_bytes):
        return b"".join(token_bytes[token_id] for token_id in ids).decode("utf-8")


    merges, token_bytes = train_byte_bpe(train_texts, max_merges=64)
    bpe_ids = bpe_encode(held_out, merges)
    assert bpe_decode(bpe_ids, token_bytes) == held_out
    assert all(0 <= token_id < len(token_bytes) for token_id in bpe_ids)
    print("Learned vocabulary:", len(token_bytes))
    print("Held-out token count: byte =", len(byte_ids), ", BPE =", len(bpe_ids))
    print("First 12 learned tokens:", [repr(t.decode("utf-8", errors="replace")) for t in token_bytes[256:268]])
    """),
    markdown("""
    ## 4. Controlled comparison: vocabulary size vs. length and parameters

    We vary only the number of learned merges. The held-out text and embedding width stay fixed. Byte-level BPE has zero `<UNK>` rate at every setting because every string can fall back to bytes. Token count on one short sample need not decrease at *every* merge: a merge learned on training text may simply not appear in the held-out text.
    """),
    code("""
    import matplotlib.pyplot as plt

    D_MODEL = 64
    merge_budgets = [0, 8, 16, 32, 64]
    rows = []
    for budget in merge_budgets:
        learned_merges, learned_bytes = train_byte_bpe(train_texts, budget)
        ids = bpe_encode(held_out, learned_merges)
        assert bpe_decode(ids, learned_bytes) == held_out
        rows.append((len(learned_bytes), len(ids), len(learned_bytes) * D_MODEL, 0))

    print("vocab | held-out tokens | embedding params | UNK count")
    for vocab, count, params, unk in rows:
        print(f"{vocab:5d} | {count:15d} | {params:16d} | {unk:9d}")

    fig, axes = plt.subplots(1, 2, figsize=(10, 3.5))
    axes[0].plot([r[0] for r in rows], [r[1] for r in rows], marker="o")
    axes[0].set(xlabel="Vocabulary size", ylabel="Held-out token count", title="Sequence length")
    axes[1].plot([r[0] for r in rows], [r[2] for r in rows], marker="o", color="darkorange")
    axes[1].set(xlabel="Vocabulary size", ylabel="Parameters", title=f"Embedding table (D={D_MODEL})")
    for ax in axes:
        ax.grid(alpha=0.25)
    plt.tight_layout()
    plt.show()
    """),
    markdown("""
    ## 5. IDs → embeddings → logits → next-token loss

    For a batch of IDs `[B,T]`, an embedding table `[V,D]` returns `[B,T,D]`. A linear LM head with weights `[V,D]` produces logits `[B,T,V]`. To train next-token prediction, position `t` predicts the ID at position `t+1`. The model below has **no context mixing**, so each prediction depends only on the current token ID.
    """),
    code("""
    import torch
    from torch import nn
    from torch.nn import functional as F

    torch.manual_seed(SEED)

    class TokenToLogits(nn.Module):
        def __init__(self, vocab_size, d_model, tie_weights=False):
            super().__init__()
            self.embedding = nn.Embedding(vocab_size, d_model)
            self.lm_head = nn.Linear(d_model, vocab_size, bias=False)
            if tie_weights:
                self.lm_head.weight = self.embedding.weight

        def forward(self, token_ids):
            embeddings = self.embedding(token_ids)
            return embeddings, self.lm_head(embeddings)


    vocab_size = len(token_bytes)
    model = TokenToLogits(vocab_size, D_MODEL)
    sample_ids = bpe_encode((held_out + " ") * 4, merges)
    assert len(sample_ids) >= 32
    batch = torch.tensor([sample_ids[:16], sample_ids[16:32]], dtype=torch.long)
    embeddings, logits = model(batch)
    assert batch.shape == (2, 16)
    assert embeddings.shape == (2, 16, D_MODEL)
    assert logits.shape == (2, 16, vocab_size)

    targets = batch[:, 1:].contiguous()
    predicted_logits = logits[:, :-1, :].contiguous()
    loss = F.cross_entropy(predicted_logits.reshape(-1, vocab_size), targets.reshape(-1))
    probabilities = torch.softmax(logits[0, -1], dim=-1)
    assert torch.isclose(probabilities.sum(), torch.tensor(1.0))
    print("IDs:", tuple(batch.shape))
    print("Embeddings:", tuple(embeddings.shape))
    print("Logits:", tuple(logits.shape))
    print("Shifted target IDs:", tuple(targets.shape))
    print("Initial next-token loss:", round(loss.item(), 4))
    """),
    markdown("""
    ## 6. Parameter ledger and weight tying

    With no biases, separate embedding and LM-head matrices contain `V×D + V×D = 2VD` parameters. Weight tying reuses the *same* `[V,D]` matrix, leaving `VD` distinct trainable parameters. The transpose is implicit in the linear layer's matrix multiplication; no second copy is stored. Real decoder-only LMs insert contextual layers between these boundaries.
    """),
    code("""
    untied = model
    tied = TokenToLogits(vocab_size, D_MODEL, tie_weights=True)
    count = lambda module: sum(p.numel() for p in module.parameters())
    assert count(untied) == 2 * vocab_size * D_MODEL
    assert count(tied) == vocab_size * D_MODEL
    assert tied.embedding.weight is tied.lm_head.weight
    print("V, D:", vocab_size, D_MODEL)
    print("Untied parameters:", count(untied))
    print("Tied parameters:", count(tied))
    """),
    markdown("""
    ## 7. Small training sanity check

    The corpus is deliberately repetitive. This is only a check that the loss and optimization path work; the model cannot use multi-token context. Day 4 builds a contextual Tiny GPT.
    """),
    code("""
    torch.manual_seed(SEED)
    training_text = " ".join(train_texts) * 3
    training_ids = torch.tensor(bpe_encode(training_text, merges), dtype=torch.long)
    optimizer = torch.optim.AdamW(model.parameters(), lr=0.01)
    losses = []
    for step in range(60):
        starts = torch.randint(0, len(training_ids) - 17, (16,))
        windows = torch.stack([training_ids[s:s + 17] for s in starts])
        inputs, targets = windows[:, :-1], windows[:, 1:]
        _, logits = model(inputs)
        loss = F.cross_entropy(logits.reshape(-1, vocab_size), targets.reshape(-1))
        optimizer.zero_grad()
        loss.backward()
        optimizer.step()
        losses.append(loss.item())

    plt.figure(figsize=(6, 3))
    plt.plot(losses)
    plt.xlabel("Optimization step")
    plt.ylabel("Next-token cross-entropy")
    plt.title("Bigram-like baseline: training sanity check")
    plt.grid(alpha=0.25)
    plt.show()
    print("First loss:", round(losses[0], 4), "Last loss:", round(losses[-1], 4))
    """),
    markdown("""
    ## 8. Record what you learned

    1. Draw the shape path: `[B,T] → [B,T,D] → [B,T,V]`.
    2. Explain why byte-level BPE has no `<UNK>`, even for the held-out emoji.
    3. Report how vocabulary size changed held-out token count and embedding parameters. Distinguish observations from what the plot cannot establish.
    4. Explain why this baseline cannot use the whole context, and which later module will fix that.

    **Reproducibility:** Fixed seed and corpus are in cells 1 and 5. The figures are generated from the notebook data, not copied from external results.
    """),
]


notebook = {
    "cells": cells,
    "metadata": {
        "colab": {"provenance": []},
        "kernelspec": {"display_name": "Python 3", "language": "python", "name": "python3"},
        "language_info": {"name": "python"},
    },
    "nbformat": 4,
    "nbformat_minor": 5,
}

OUTPUT.write_text(json.dumps(notebook, ensure_ascii=False, indent=1) + "\n", encoding="utf-8")
print(OUTPUT)
