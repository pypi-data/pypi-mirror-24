=========
RexPython
=========

This is Reactive Extensions (Rx) for Python implementation mimicing RxJava2 API as far as it can.
It is LINQ free btw. The goal to make it hackable on the go.

https://github.com/chexov/rexpython


Installation
============
pip install rexpython

=====
Usage
=====
import rexpython as rx

def on_subscribe(emitter):
    emitter.setDisposable(ActionDisposable(lambda: sys.stdout.write("disposed")))

    print ("subscribed")
    for i in xrange(1, 3):
        emitter.onNext(i)
        time.sleep(1)

    # emitter.onError(Exception("foo"))
    emitter.onComplete()

frames = rx.Observable.create(lambda emitter: on_subscribe(emitter, video_url, 2))
mat_img = frames.map(featureextractor.FeatureExtractor.preprocess_image)
vect = mat_img.map(lambda img: fe.get_activations([img]))
words = vect.map(lambda vec: d.getWordsForBatch(vec, 40)) \
    .flatMap(lambda wlist: rx.Observable.from_(wlist))
words = words.doOnNext(lambda w: log.info("words=%s" % w)).doOnError(lambda err: log.error("ERRRORRR %s" % err))
value = words.toList().blockingGet()
